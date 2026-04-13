from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json


class HuggingFaceLLM:
    def __init__(self, model_name, max_tokens=512):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.max_tokens = max_tokens

    def generate(self, prompt: str) -> dict:
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_tokens,
            temperature=0.0
        )

        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # extract JSON (important)
        try:
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            return json.loads(text[json_start:json_end])
        except Exception:
            raise ValueError("HF model did not return valid JSON")


class OpenAILLM:
    def __init__(self, model_name):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model_name

    def generate(self, prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": "Return strict JSON only"},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content
        return json.loads(content)