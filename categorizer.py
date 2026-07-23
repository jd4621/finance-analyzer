import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


CATEGORIES = {
    "Food & Groceries", "Transport", "Entertainment", "Utilities", "Health",
    "Education", "Rent", "Savings", "Income", "Other",
}


def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured. Add it to your .env file.")
    return Groq(api_key=api_key)


def categorize_transactions(descriptions: list) -> dict:
    if not descriptions:
        return {}

    client = _get_client()
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

    raw = response.choices[0].message.content or ""
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        categories = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError("The categorization service returned an invalid response.") from error

    if not isinstance(categories, dict):
        raise RuntimeError("The categorization service returned an unexpected response.")

    return {
        description: category if category in CATEGORIES else "Other"
        for description, category in categories.items()
        if description in descriptions
    }
