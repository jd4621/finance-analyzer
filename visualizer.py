import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "primary": "#7c83fd",
    "danger": "#e74c3c",
    "success": "#2ecc71",
    "warning": "#f39c12",
    "palette": ["#7c83fd", "#2ecc71", "#f39c12", "#e74c3c",
                "#a8b2d8", "#fd7c83", "#7cfda8", "#fdd97c"]
}

def spending_by_category_chart(df: pd.DataFrame):
    expenses = df[df["Type"] == "Expense"].groupby("Category")["AbsAmount"].sum().reset_index()
    fig = px.pie(
        expenses,
        values="AbsAmount",
        names="Category",
        title="Spending by Category",
        hole=0.5,
        color_discrete_sequence=COLORS["palette"]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8b2d8"),
        legend=dict(orientation="h", y=-0.2),
        title_font=dict(size=16, color="#ffffff"),
    )

    return fig

def spending_over_time_chart(df: pd.DataFrame):
    daily = df[df["Type"] == "Expense"].groupby("Date")["AbsAmount"].sum().reset_index()

    fig = px.area(
        daily,
        x="Date",
        y="AbsAmount",
        title="Daily Spending over Time",
        labels={"ABsAmount": "Amount (KES)", "Date": "Date"},
    )

    fig.update_traces(
        line_color=COLORS["danger"],
        fillcolor="rgba(231, 76, 60, 0.2)"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8b2d8"),
        title_font=dict(size=16, color="#ffffff"),
        xaxis=dict(gridcolor="#2d3250"),
        yaxis=dict(gridcolor="#2d3250"),

    )

    return fig


def top_expenses_chart(df: pd.DataFrame):
    top = df[df["Type"] == "Expense"].nlargest(10, "AbsAmount")
    fig = px.bar(
        top,
        x="AbsAmount",
        y="Description",
        orientation="h",
        title="Top 10 Expenses",
        labels={"AbsAMount": "Amount (KES)", "Description": ""},
        color="AbsAmount",
        color_continuous_scale=["#7c83fd", "#e74c3c"]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8b2db"),
        title_font=dict(size=16, color="#ffffff"),
        xaxis=dict(gridcolor="#2d3250"),
        yaxis=dict(gridcolor="#2d3250"),
        coloraxis_showscale=False,
    )             # Red bars for expenses
    return fig


def monthly_comparison_chart(df: pd.DataFrame):
    df = df.copy()
    df["Month"] = df["Date"].dt.strftime("%b %Y")

    monthly = df[df["Type"] == "Expense"].groupby(
        ["Month", "Category"]
    )["AbsAmount"].sum().reset_index()

    fig = px.bar(
        monthly,
        x="Month",
        y="AbsAmount",
        color="Category",
        title="Monthly Spending by Category",
        labels={"AbsAmount": "Amount (KES)", "Month": ""},
        barmode="stack",
        color_discrete_sequence=COLORS["palette"],
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8b2d8"),
        title_font=dict(size=16, color="#ffffff"),
        xaxis=dict(gridcolor="#2d3250"),
        yaxis=dict(gridcolor="#2d3250"),
        legend=dict(orientation="h", y=0.3)
    )

    return fig