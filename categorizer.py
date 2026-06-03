import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def categorize_transactions(descriptions: list) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    descriptions_text = "\n".join([f"- {d}" for d in descriptions])

    prompt = f"""Categorize each of these bank transaction descriptions into one of these categories:
Food & Groceries, Transport, Entertainment, Utilities, Health, Education, Rent, Savings, Income, Other.

Return ONLY a valid JSON object mapping each description exactly to its category.
No explanation, no markdown, just JSON object.

Transactions:
{descriptions_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    return json.loads(raw)