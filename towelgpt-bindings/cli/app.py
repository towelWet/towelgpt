"""towelgpt CLI

The towelgpt CLI is a self-contained script based on the `towelgpt` and `typer` packages. It offers a
REPL to communicate with a language model similar to the chat GUI application, but more basic.
"""

import io
import pkg_resources  # should be present as a dependency of towelgpt
import sys
import typer

from collections import namedtuple
from typing_extensions import Annotated
from towelgpt import towelgpt


MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello there."},
    {"role": "assistant", "content": "Hi, how can I help you?"},
]

SPECIAL_COMMANDS = {
    "/reset": lambda messages: messages.clear(),
    "/exit": lambda _: sys.exit(),
    "/clear": lambda _: print("\n" * 100),
    "/help": lambda _: print("Special commands: /reset, /exit, /help and /clear"),
}

VersionInfo = namedtuple('VersionInfo', ['major', 'minor', 'micro'])
VERSION_INFO = VersionInfo(1, 0, 2)
VERSION = '.'.join(map(str, VERSION_INFO))  # convert to string form, like: '1.2.3'

CLI_START_MESSAGE = f"""
    
 ██████  ██████  ████████ ██   ██  █████  ██      ██      
██       ██   ██    ██    ██   ██ ██   ██ ██      ██      
██   ███ ██████     ██    ███████ ███████ ██      ██      
██    ██ ██         ██         ██ ██   ██ ██      ██      
 ██████  ██         ██         ██ ██   ██ ███████ ███████ 
                                                          

Welcome to the towelgpt CLI! Version {VERSION}
Type /help for special commands.
                                                    
"""

# create typer app
app = typer.Typer()

@app.command()
def repl(
    model: Annotated[
        str,
        typer.Option("--model", "-m", help="Model to use for chatbot"),
    ] = "ggml-towelgpt-j-v1.3-groovy",
    n_threads: Annotated[
        int,
        typer.Option("--n-threads", "-t", help="Number of threads to use for chatbot"),
    ] = None,
):
    """The CLI read-eval-print loop."""
    towelgpt_instance = towelgpt(model)

    # if threads are passed, set them
    if n_threads is not None:
        num_threads = towelgpt_instance.model.thread_count()
        print(f"\nAdjusted: {num_threads} →", end="")

        # set number of threads
        towelgpt_instance.model.set_thread_count(n_threads)

        num_threads = towelgpt_instance.model.thread_count()
        print(f" {num_threads} threads", end="", flush=True)
    else:
        print(f"\nUsing {towelgpt_instance.model.thread_count()} threads", end="")

    print(CLI_START_MESSAGE)

    use_new_loop = False
    try:
        version = pkg_resources.Environment()['towelgpt'][0].version
        version_major = int(version.split('.')[0])
        if version_major >= 1:
            use_new_loop = True
    except:
        pass  # fall back to old loop
    if use_new_loop:
        _new_loop(towelgpt_instance)
    else:
        _old_loop(towelgpt_instance)


def _old_loop(towelgpt_instance):
    while True:
        message = input(" ⇢  ")

        # Check if special command and take action
        if message in SPECIAL_COMMANDS:
            SPECIAL_COMMANDS[message](MESSAGES)
            continue

        # if regular message, append to messages
        MESSAGES.append({"role": "user", "content": message})

        # execute chat completion and ignore the full response since 
        # we are outputting it incrementally
        full_response = towelgpt_instance.chat_completion(
            MESSAGES,
            # preferential kwargs for chat ux
            logits_size=0,
            tokens_size=0,
            n_past=0,
            n_ctx=0,
            n_predict=200,
            top_k=40,
            top_p=0.9,
            temp=0.9,
            n_batch=9,
            repeat_penalty=1.1,
            repeat_last_n=64,
            context_erase=0.0,
            # required kwargs for cli ux (incremental response)
            verbose=False,
            streaming=True,
        )
        # record assistant's response to messages
        MESSAGES.append(full_response.get("choices")[0].get("message"))
        print() # newline before next prompt


def _new_loop(towelgpt_instance):
    with towelgpt_instance.chat_session():
        while True:
            message = input(" ⇢  ")

            # Check if special command and take action
            if message in SPECIAL_COMMANDS:
                SPECIAL_COMMANDS[message](MESSAGES)
                continue

            # if regular message, append to messages
            MESSAGES.append({"role": "user", "content": message})

            # execute chat completion and ignore the full response since 
            # we are outputting it incrementally
            response_generator = towelgpt_instance.generate(
                message,
                # preferential kwargs for chat ux
                max_tokens=200,
                temp=0.9,
                top_k=40,
                top_p=0.9,
                repeat_penalty=1.1,
                repeat_last_n=64,
                n_batch=9,
                # required kwargs for cli ux (incremental response)
                streaming=True,
            )
            response = io.StringIO()
            for token in response_generator:
                print(token, end='', flush=True)
                response.write(token)

            # record assistant's response to messages
            response_message = {'role': 'assistant', 'content': response.getvalue()}
            response.close()
            towelgpt_instance.current_chat_session.append(response_message)
            MESSAGES.append(response_message)
            print() # newline before next prompt


@app.command()
def version():
    """The CLI version command."""
    print(f"towelgpt-cli v{VERSION}")


if __name__ == "__main__":
    app()
