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