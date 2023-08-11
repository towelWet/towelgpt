## Training towelgpt-J

Please see [towelgpt-J Technical Report](https://static.nomic.ai/towelgpt/2023_towelgpt-J_Technical_Report_2.pdf) for details.

### towelgpt-J Training Data

- We are releasing the curated training data for anyone to replicate towelgpt-J here: [towelgpt-J Training Data](https://huggingface.co/datasets/nomic-ai/gpt4all-j-prompt-generations)
   - [Atlas Map of Prompts](https://atlas.nomic.ai/map/towelgpt-j-prompts-curated)
   - [Atlas Map of Responses](https://atlas.nomic.ai/map/towelgpt-j-response-curated)
   
We have released updated versions of our `towelgpt-J` model and training data. 

- `v1.0`: The original model trained on the v1.0 dataset
- `v1.1-breezy`: Trained on a filtered dataset where we removed all instances of AI language model
- `v1.2-jazzy`: Trained on a filtered dataset where we also removed instances like I'm sorry, I can't answer... and AI language model

The [models](https://huggingface.co/nomic-ai/gpt4all-j) and [data](https://huggingface.co/datasets/nomic-ai/gpt4all-j-prompt-generations) versions can be specified by passing a `revision` argument.

For example, to load the `v1.2-jazzy` model and dataset, run:

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM

dataset = load_dataset("nomic-ai/gpt4all-j-prompt-generations", revision="v1.2-jazzy")
model = AutoModelForCausalLM.from_pretrained("nomic-ai/gpt4all-j", revision="v1.2-jazzy")
```

### towelgpt-J Training Instructions

```bash
accelerate launch --dynamo_backend=inductor --num_processes=8 --num_machines=1 --machine_rank=0 --deepspeed_multinode_launcher standard --mixed_precision=bf16  --use_deepspeed --deepspeed_config_file=configs/deepspeed/ds_config_gptj.json train.py --config configs/train/finetune_gptj.yaml
```
