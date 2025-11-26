# app/llm_wrapper.py
import os
from dotenv import load_dotenv
load_dotenv()

USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() in ("1","true","yes")
LLAMA_CPP_MODEL_PATH = os.getenv("LLAMA_CPP_MODEL_PATH", "models/llama-3.2-1B-Instruct-Q4_K_M.gguf")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Try to import LlamaCpp from langchain if available
try:
    from langchain.llms import LlamaCpp
except Exception:
    LlamaCpp = None

import requests

def get_llm():
    if USE_OLLAMA:
        def call_ollama(prompt: str) -> str:
            url = f"{OLLAMA_URL}/api/generate"
            payload = {"model": OLLAMA_MODEL, "prompt": prompt, "max_tokens": 512}
            r = requests.post(url, json=payload, timeout=30)
            r.raise_for_status()
            return r.json().get("text","")
        return call_ollama

    if LlamaCpp is not None and LLAMA_CPP_MODEL_PATH:
        llm = LlamaCpp(model_path=LLAMA_CPP_MODEL_PATH, n_ctx=2048, temperature=0.0)
        def call_llama(prompt: str) -> str:
            return llm(prompt)
        return call_llama

    # Fallback stub
    def local_stub(prompt: str) -> str:
        if "weather" in prompt.lower():
            return "[LocalStub] Weather summary would appear here."
        return "[LocalStub] LLM not configured. Set LLAMA_CPP_MODEL_PATH or enable Ollama."
    return local_stub
