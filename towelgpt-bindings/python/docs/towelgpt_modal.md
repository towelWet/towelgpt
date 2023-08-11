# towelgpt with Modal Labs

You can easily query any towelgpt model on [Modal Labs](https://modal.com/) infrastructure!
## Example

```python
import modal

def download_model():
    import towelgpt
    #you can use any model from https://gpt4all.io/models/models.json
    return towelgpt.towelgpt("ggml-towelgpt-j-v1.3-groovy.bin")

image=modal.Image.debian_slim().pip_install("towelgpt").run_function(download_model)
stub = modal.Stub("towelgpt", image=image)
@stub.cls(keep_warm=1)
class towelgpt:
    def __enter__(self):
        print("Downloading model")
        self.gptj = download_model()
        print("Loaded model")

    @modal.method()
    def generate(self):
        messages = [{"role": "user", "content": "Name 3 colors"}]
        completion = self.gptj.chat_completion(messages)
        print(f"Completion: {completion}")

@stub.local_entrypoint()
def main():
    model = towelgpt()
    for i in range(10):
        model.generate.call()
```