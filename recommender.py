import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_recommendations(summary: dict, category_totals: dict) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    categories_text = "\n".join([
        f"- {category}: KES {amount:,.0f}"
        for category, amount in sorted(category_totals.items(),
        key=lambda x: x[1], reverse=True)
    ])

    prompt = f"""You are a personal finance advisor. Analyze this person's monthly spending and give practical advice.

Financial Summary:
- Total Income: KES {summary['total_income']:,.0f}
- Total Expenses: KES {summary['total_expenses']:,.0f}
- Net Savings: KES {summary['net_savings']:,.0f}
- Number of transactions: {summary['transaction_count']}

Spending by Category:
{categories_text}

Give exactly 5 specific, actionable recommendations to help this person save more money.
Be direct and specific -  mention actual amounts and categories from their data.
Format each recommendation as a numbered list starting with 1."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content