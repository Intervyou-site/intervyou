import os, json, httpx, numpy as np
from typing import List

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_EMBED_URL = "https://api.openai.com/v1/embeddings"

async def call_llm_chat(system_prompt: str, user_message: str, model="gpt-4o-mini", max_tokens=400, temperature=0.2):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type":"application/json"}
    payload = {
        "model": model,
        "messages":[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_message}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(OPENAI_CHAT_URL, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

async def get_embeddings(texts: List[str], model="text-embedding-3-small"):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type":"application/json"}
    payload = {"input": texts, "model": model}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(OPENAI_EMBED_URL, json=payload, headers=headers)
        r.raise_for_status()
        js = r.json()
        # returns list of vectors
        return [item["embedding"] for item in js["data"]]
