import pandas as pd

def load_statement(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Amount"] = (
        df["Amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(r"[^0-9.-]", "", regex=True)
    )
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Type"] = df["Amount"].apply(
        lambda x: "Income" if x > 0 else "Expense"
    )
    df["AbsAmount"] = df["Amount"].abs()

    return df

def get_summary(df: pd.DataFrame) -> dict:
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expenses = abs(df[df["Type"] == "Expense"]["Amount"].sum())

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": total_income - total_expenses,
        "expense_count": len(df[df["Type"] == "Expense"]),
    }