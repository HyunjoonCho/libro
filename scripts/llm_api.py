import os
import json
import requests
import random

import openai
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, StoppingCriteria, StoppingCriteriaList

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)
HF_KEY = os.getenv("HUGGINGFACE_TOKEN")

AVAILABLE_MODEL_INFO = {
    'OpenAI/gpt-4o': {
        'query_type': 'openai',
        'uses_chat': True,
    },
    'meta-llama/Meta-Llama-3-8B-Instruct': {
        'query_type': 'hf_transformers',
        'uses_chat': True,
    },
    'meta-llama/Meta-Llama-3.1-8B-Instruct': {
        'query_type': 'hf_transformers',
        'uses_chat': True,
    },
    'mistralai/Mistral-Nemo-Instruct-2407': {
        'query_type': 'hf_transformers',
        'uses_chat': True,
    },
    'Qwen/Qwen2.5-Coder-7B-Instruct': {
        'query_type': 'hf_transformers',
        'uses_chat': True,
    },
    'microsoft/phi-4': {
        'query_type': 'hf_transformers',
        'uses_chat': True,
    },
}
AVAILABLE_MODELS = AVAILABLE_MODEL_INFO.keys() # just for clean code

TEMP = 0.7

# Helper functions

def model_is_chat(model):
    return AVAILABLE_MODEL_INFO[model]['uses_chat']

def tiny_noise(scale=1/1000):
    return scale*random.random()-0.5*scale

class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_strings, tokenizer):
        self.stop_strings = stop_strings
        self.tokenizer = tokenizer
    
    def __call__(self, input_ids, scores, **kwargs):
       decoded = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
       return any(stop in decoded for stop in self.stop_strings)

# Query functions
class ModelWrapper:
    _model_name = None
    _model = None
    _tokenizer = None
    _generator = None
    
    @classmethod
    def generate(cls, prompt, model_name, stop_tokens, use_cache=False):
        if not cls._generator or cls._model_name != model_name:
            cls._model_name = model_name
            cls._model = AutoModelForCausalLM.from_pretrained(model_name, token=HF_KEY, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map='auto')
            cls._tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_KEY, trust_remote_code=True)
            cls._generator = pipeline("text-generation",model=cls._model, tokenizer=cls._tokenizer, torch_dtype=torch.bfloat16, device_map='auto', token=HF_KEY)

        use_temp = TEMP if use_cache else (TEMP + tiny_noise())
        prompt = cls._generator.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
        stopping_criteria = None
        if stop_tokens:
            stopping_criteria = StoppingCriteriaList([StopOnTokens(stop_tokens, cls._tokenizer)])

        generated_text = cls._generator(prompt, temperature=use_temp, stopping_criteria=stopping_criteria, return_full_text=False)[0]['generated_text']
        cost = {
            'prompt_tokens': len(cls._tokenizer.encode(prompt)),
            'completion_tokens': len(cls._tokenizer.encode(generated_text)),
        }

        return generated_text, cost

def query_chat_llm(prompt, model, stop_tokens):
    assert model in AVAILABLE_MODEL_INFO, f'Unknown model {model}'
    model_info = AVAILABLE_MODEL_INFO[model]
    assert type(prompt) == list
    assert model_info['uses_chat']

    if model_info['query_type'] == 'openai':
        base_model_name = model.split('/')[-1]
        response = client.chat.completions.create(
            model=base_model_name,
            messages=prompt, # chat-style prompt
            n=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_tokens
        )
        gen_result = response.choices[0].message.content
        cost = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
        }
        if gen_result and "```" in gen_result:
            parts = gen_result.split("```")
            if len(parts) >= 2:
                gen_result = parts[1]
                gen_result = gen_result.removeprefix('java')
    elif model_info['query_type'] == 'hf_transformers':
        gen_result, cost = ModelWrapper.generate(prompt, model, stop_tokens)
    else:
        raise NotImplementedError(f'Unknown query type {model_info["query_type"]}')
    return gen_result, cost

def query_string_llm(prompt, model, stop_tokens):
    assert model in AVAILABLE_MODEL_INFO, f'Unknown model {model}'
    model_info = AVAILABLE_MODEL_INFO[model]
    assert type(prompt) == str
    assert not model_info['uses_chat']

    return "", {}

def query_llm(prompt, model, stop_tokens):
    # sanity checks
    assert model in AVAILABLE_MODELS, f'Unknown model {model}'
    model_info = AVAILABLE_MODEL_INFO[model]
    if model_info['uses_chat']:
        assert type(prompt) == list
    else:
        assert type(prompt) == str
    
    # actual execution
    query_func = query_chat_llm if model_info['uses_chat'] else query_string_llm
    return query_func(prompt, model, stop_tokens)
