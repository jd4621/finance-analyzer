import plotly.express as px
import pandas as pd

def spending_by_category_chart(df: pd.DataFrame):
    expenses = df[df["Type"] == "Expense"].groupby("Category")["AbsAmount"].sum().reset_index()
    fig = px.pie(
        expenses,
        values="AbsAmount",
        names="Category",
        title="Spending by Category",
        hole=0.4
    )

    fig.update_layout(
        legend=dict(orientation="h", y=-0.2)
    )

    return fig

def spending_over_time_chart(df: pd.DataFrame):
    daily = df[df["Type"] == "Expense"].groupby("Date")["AbsAmount"].sum().reset_index()
    fig = px.line(
        daily,
        x="Date",
        y="AbsAmount",
        title="Daily Spending over Time",
        labels={"ABsAmount": "Amount (KES)", "Date": "Date"},
    )

    fig.update_traces(line_color="#e74c3c")                 # Red lines for expenses
    return fig


def top_expenses_chart(df: pd.DataFrame):
    top = df[df["Type"] == "Expense"].nlargest(10, "AbsAmount")
    fig = px.bar(
        x="AbsAmount",
        y="Description",
        orientation="h",
        title="Top 10 Expenses",
        labels={"AbsAMount": "Amount (KES)", "Description": ""},
    )

    fig.update_traces(marker_color="#e74c3c")             # Red bars for expenses
    return fig