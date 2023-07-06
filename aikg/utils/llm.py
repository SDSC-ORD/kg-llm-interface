import re
from typing import Any, List, Mapping, Optional

from langchain import HuggingFacePipeline, LLMChain, PromptTemplate
import torch
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import aikg.config.chat


def setup_llm(model_id: str, max_new_tokens: int):
    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tok,
        max_new_tokens=max_new_tokens,
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm


def setup_llm_chain(llm: HuggingFacePipeline, prompt_template: str) -> LLMChain:
    """Prepare the prompt injection and text generation system."""
    # Auto-detecting prompt variables surrounded by single curly braces
    variables = re.findall(r'[^{]{([^}]+)}[^}]', prompt_template)
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=variables,
    )
    return LLMChain(prompt=prompt, llm=llm)
