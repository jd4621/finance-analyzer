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