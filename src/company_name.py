import pandas as pd


INTERIM_IN  = "data/interim/02_after_job_title.csv"
INTERIM_OUT = "data/interim/03_after_company.csv"


def extract_company_name(value: str) -> str:
    """
    Extracts the company name from the Glassdoor format.
    """
    if pd.isna(value):
        return None

    return value.split("\n")[0].strip()


def clean_company(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the company column by extracting only the company name.
    """
    df["Company Name"] = df["Company Name"].apply(extract_company_name)

    return df


def report(df: pd.DataFrame) -> None:
    print(f"\n[company] Unique companies: {df['Company Name'].nunique()}")


def save(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"[company] Saved to: {path}")


def run(df: pd.DataFrame = None) -> pd.DataFrame:
    
    if df is None:
        df = pd.read_csv(INTERIM_IN)

    df = clean_company(df)
    report(df)
    save(df, INTERIM_OUT)

    return df


if __name__ == "__main__":
    run()