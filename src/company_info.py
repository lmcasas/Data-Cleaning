import pandas as pd


INTERIM_IN  = "data/interim/05_after_job_description.csv"
INTERIM_OUT = "data/interim/06_after_company_info.csv"

# Columns that use -1 as a null value
COLUMNS_WITH_SENTINEL = [
    "Headquarters", 
    "Size", 
    "Founded", 
    "Type of ownership", 
    "Industry", 
    "Sector", 
    "Revenue", 
    "Competitors", 
    "Rating" 
]


def replace_sentinel(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Replaces -1 (string or numeric) with Unknown/0 in the specified columns.
    Glassdoor uses -1 to indicate unknown data.
    """
    for col in columns:
        if col not in df.columns:
            print(f"[company_info]  Column not found: '{col}' — skipping")
            continue

        before = (df[col].astype(str).str.strip() == "-1").sum()

        df[col] = df[col].replace("-1", "Unknown")  
        df[col] = df[col].replace(-1, pd.NA)      
    return df


def clean_null(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(subset=["Founded"], inplace=True)
    df.dropna(subset=["Rating"], inplace=True)
    return df


def report(df: pd.DataFrame) -> None:

    if "Size" in df.columns:
        print("\n[company_info] Size distribution:")
        print(df["Size"].value_counts(dropna=False))

    if "Sector" in df.columns:
        print("\n[company_info] Sector distribution:")
        print(df["Sector"].value_counts(dropna=False))

    if "Founded" in df.columns:
        print("\n[company_info] Year founded (Founded):")
        print(df["Founded"].value_counts(dropna=False))

    if "Headquarters" in df.columns:
        print("\n[company_info] Headquarters:")
        print(df["Headquarters"].value_counts(dropna=False))
    
    if "Rating" in df.columns:
        print("\n[company_info] Rating distribution:")
        print(df["Rating"].value_counts(dropna=False))

    if "Type of ownership" in df.columns:
        print("\n[company_info] Ownership type:")
        print(df["Type of ownership"].value_counts(dropna=False))

    if "Industry" in df.columns:
        print("\n[company_info] Industry distribution:")
        print(df["Industry"].value_counts(dropna=False))

    if "Revenue" in df.columns:
        print("\n[company_info] Revenue distribution:")
        print(df["Revenue"].value_counts(dropna=False))
    
    if "Competitors" in df.columns:
        print("\n[company_info] Competitors distribution:")
        print(df["Competitors"].value_counts(dropna=False))


def save(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"\n[company_info] Saved to: {path}")


def run(df: pd.DataFrame = None) -> pd.DataFrame:

    if df is None:
        df = pd.read_csv(INTERIM_IN)

    df = replace_sentinel(df, COLUMNS_WITH_SENTINEL)
    df = clean_null(df)
    #report(df)
    save(df, INTERIM_OUT)
    return df


if __name__ == "__main__":
    run()