import pandas as pd

RAW_PATH = "data/raw/Uncleaned_DS_jobs.csv"
INTERIM_PATH = "data/interim/01_after_ingest.csv"


def load(path: str) -> pd.DataFrame:
    """
    Loads the raw dataset and removes the 'index' column if it exists.
    """
    df = pd.read_csv(path)

    if "index" in df.columns:
        df = df.drop(columns=["index"])

    print(f"[ingest] Rows loaded: {len(df)} | Columns ({len(df.columns)}): {list(df.columns)}")

    return df


def report(df: pd.DataFrame) -> None:
    """
    Displays basic data quality information.
    """
    print("\n── Null values per column ──")
    print(df.isnull().sum())

    n_dup = df.duplicated().sum()

    print(f"\n── Duplicate rows: {n_dup} ──")

    if n_dup > 0:
        print(df[df.duplicated()])


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate rows from the dataset.
    """
    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    print(f"[ingest] Duplicates removed: {removed} | Remaining rows: {len(df)}")

    return df


def save(df: pd.DataFrame, path: str) -> None:
    """
    Saves the cleaned dataset to the interim folder.
    """
    df.to_csv(path, index=False)

    print(f"[ingest] Saved to: {path}")


def run() -> pd.DataFrame:

    df = load(RAW_PATH)
    report(df)
    df = remove_duplicates(df)
    save(df, INTERIM_PATH)

    return df


if __name__ == "__main__":
    run()