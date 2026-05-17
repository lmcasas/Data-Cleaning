import pandas as pd
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d")

filename = f"DS_jobs_clean_{timestamp}.csv"


INTERIM_IN = "data/interim/06_after_company_info.csv"
PROCESSED_OUT = f"data/processed/{filename}"
LATEST_OUT = "data/processed/latest.csv"

EXPECTED_COLUMNS = [
    "Job Title", "Title", "Job_category", "Level",
    "Location", "Company Name", "Job Description", "Rating",
    "Salary_Min", "Salary_Max", "Salary_Avg", "Salary_Source",
    "Headquarters", "Size", "Founded", "Type of ownership",
    "Industry", "Sector", "Revenue", "Competitors",
]


NOT_NULL_COLUMNS = [
    "Title",
    "Job_category",
    "Level",
    "Salary_Min",
    "Salary_Max",
]


SALARY_VALID = (0, 500_000)
RATING_VALID = (0.0, 5.0)


# Validation Functions 

def check_columns(df: pd.DataFrame) -> bool:
    """Ensure all expected columns exist."""
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]

    if missing:
        print(f"[validate]  Missing columns: {missing}")
        return False

    print(f"[validate] All expected columns present ({len(EXPECTED_COLUMNS)})")
    return True


def check_nulls(df: pd.DataFrame) -> bool:
    """Check that critical columns do not contain null values."""
    failed = False

    for col in NOT_NULL_COLUMNS:
        if col not in df.columns:
            print(f"[validate]  Column '{col}' missing (cannot check nulls)")
            failed = True
            continue

        n = df[col].isna().sum()

        if n > 0:
            print(f"[validate]  '{col}' has {n} unexpected nulls")
            failed = True
        else:
            print(f"[validate] '{col}' has no nulls")

    return not failed


def check_ranges(df: pd.DataFrame) -> bool:
    """Validate numeric ranges for salary and rating."""
    failed = False

    if "Salary_Min" in df.columns:
        bad = df["Salary_Min"].dropna()
        bad = bad[(bad < SALARY_VALID[0]) | (bad > SALARY_VALID[1])]

        if len(bad) > 0:
            print(f"[validate]  Salary_Min out of range ({len(bad)} rows)")
            print(bad.value_counts())
            failed = True
        else:
            print("[validate] Salary_Min within range")

    if "Salary_Max" in df.columns:
        bad = df["Salary_Max"].dropna()
        bad = bad[(bad < SALARY_VALID[0]) | (bad > SALARY_VALID[1])]

        if len(bad) > 0:
            print(f"[validate]  Salary_Max out of range ({len(bad)} rows)")
            failed = True
        else:
            print("[validate] Salary_Max within range")

    if "Rating" in df.columns:
        bad = df["Rating"].dropna()
        bad = bad[(bad < RATING_VALID[0]) | (bad > RATING_VALID[1])]

        if len(bad) > 0:
            print(f"[validate]  Rating out of range ({len(bad)} rows)")
            failed = True
        else:
            print("[validate] Rating within range")

    return not failed


def summary(df: pd.DataFrame) -> None:
    """Print final dataset statistics."""
    memory_kb = df.memory_usage(deep=True).sum() / 1024

    print("\n[validate] ── Final Summary ─────────────────────")
    print(f"Rows:    {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Memory:  {memory_kb:.1f} KB")


def save(df: pd.DataFrame, path: str) -> None:
    """Save the final processed dataset."""
    df.to_csv(path, index=False)
    print(f"\n[validate] Final dataset saved to: {path}")


# ── Pipeline Step ────────────────────────────────────────────

def run(df: pd.DataFrame = None) -> pd.DataFrame:
    """Run validation checks and export final dataset."""
    if df is None:
        df = pd.read_csv(INTERIM_IN)

    print("\n[validate] ── Checking columns ─────────────────")
    check_columns(df)

    print("\n[validate] ── Checking nulls ───────────────────")
    check_nulls(df)

    print("\n[validate] ── Checking ranges ──────────────────")
    check_ranges(df)

    summary(df)

    save(df, PROCESSED_OUT)
    save(df, LATEST_OUT)

    return df


if __name__ == "__main__":
    run()