import pandas as pd

def clean_data(df):

    df.columns = df.columns.str.strip()

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df = df.dropna(subset=["Timestamp"])

    df = df.drop_duplicates()

    df["Sales Count"] = pd.to_numeric(
        df["Sales Count"],
        errors="coerce"
    )

    df["Redemption Count"] = pd.to_numeric(
        df["Redemption Count"],
        errors="coerce"
    )

    df["Sales Count"] = df["Sales Count"].fillna(0)

    df["Redemption Count"] = df["Redemption Count"].fillna(0)

    return df