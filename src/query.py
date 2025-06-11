import aiohttp
import asyncio
from .constants import OPENROUTER_API_KEY, INTERVIEW_POSTION

SYSTEM_PROMPT = f"""You are interviewing for a {INTERVIEW_POSTION} position.
You will receive an audio transcription of the question. It may not be complete. You need to understand the question and write an answer to it.\n
"""
SHORTER_INSTRACT = "Concisely respond, limiting your answer to 50 words."
LONGER_INSTRACT = (
    "Before answering, take a deep breath and think one step at a time. Believe the answer in no more than 150 words."
)

async def query_openrouter_async(transcript: str, short_answer: bool = True, temperature: float = 0.7) -> str:
    if short_answer:
        system_prompt = SYSTEM_PROMPT + SHORTER_INSTRACT
    else:
        system_prompt = SYSTEM_PROMPT + LONGER_INSTRACT

    url = "https://openrouter.ai/api/v1/chat/completions"
    model = "meta-llama/llama-3.3-8b-instruct:free"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript},
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response.raise_for_status()
            result = await response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')


