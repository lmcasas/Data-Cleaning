import pandas as pd
import re


INTERIM_IN  = "data/interim/04_after_salary.csv"
INTERIM_OUT = "data/interim/05_after_job_description.csv"


HEADERS_TO_REMOVE = [
    r"^description\s*",
    r"^job description[:\s]*",
    r"^overview[:\s]*",
    r"^about the role[:\s]*",
    r"^about this role[:\s]*",
    r"^position summary[:\s]*",
    r"^job summary[:\s]*",
    r"^function[:\s]*",
]


def clean_description(value: str) -> str:
    """
    Cleans a single job description text by:
    - Removing common headers at the beginning
    - Normalizing line breaks
    - Collapsing multiple spaces
    """
    if pd.isna(value):
        return None

    text = value.replace("\\n", " ").replace("\n", " ")

    # Remove known headers at the beginning (case insensitive)
    for pattern in HEADERS_TO_REMOVE:
        new_text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        if new_text != text:
            text = new_text
            break

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_job_description(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the 'Job Description' column:
    - Removes generic headers at the beginning
    - Normalizes line breaks and spacing
    """
    if "Job Description" not in df.columns:
        print("[job_description]  Column 'Job Description' not found")
        return df

    df["Job Description"] = df["Job Description"].apply(clean_description)

    # Detect empty rows after cleaning
    empty = df["Job Description"].isna().sum()

    if empty > 0:
        print(f"[job_description]  {empty} empty rows after cleaning")

    return df


def report(df: pd.DataFrame) -> None:
    """
    Reports basic statistics about the cleaned job descriptions.
    """
    lengths = df["Job Description"].dropna().apply(len)

    print(f"\n[job_description] Average length: {lengths.mean():.0f} characters")
    print(f"[job_description] Shortest:       {lengths.min()} characters")
    print(f"[job_description] Longest:        {lengths.max()} characters")


def save(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"[job_description] Saved to: {path}")


def run(df: pd.DataFrame = None) -> pd.DataFrame:
    
    if df is None:
        df = pd.read_csv(INTERIM_IN)

    df = clean_job_description(df)
    report(df)
    save(df, INTERIM_OUT)

    return df


if __name__ == "__main__":
    run()