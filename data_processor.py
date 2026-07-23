import pandas as pd


REQUIRED_COLUMNS = {"Date", "Description", "Amount"}


def load_statement(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(
        df["Amount"].astype(str).str.replace(",", "").str.replace("[^0-9.-]", "", regex=True),
        errors="coerce"
    )
    df = df.dropna(subset=["Date", "Amount", "Description"]).copy()
    df["Description"] = df["Description"].astype(str).str.strip()
    df = df[df["Description"].ne("")].copy()

    df["Type"] = "Neutral"
    df.loc[df["Amount"] > 0, "Type"] = "Income"
    df.loc[df["Amount"] < 0, "Type"] = "Expense"
    df["AbsAmount"] = df["Amount"].abs()
    return df


def get_summary(df: pd.DataFrame) -> dict:
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expenses = abs(df[df["Type"] == "Expense"]["Amount"].sum())

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": total_income - total_expenses,
        "transaction_count": len(df),
        "expense_count": len(df[df["Type"] == "Expense"])
    }
