import pandas as pd
import re


INTERIM_IN  = "data/interim/03_after_company.csv"
INTERIM_OUT = "data/interim/04_after_salary.csv"


def extract_salary_min(value: str) -> float:
    """
    Extracts the minimum salary from the salary estimate string.
    """
    if pd.isna(value):
        return None

    match = re.search(r"(\d+)K", value)

    if match:
        return int(match.group(1)) * 1000

    return None


def extract_salary_max(value: str) -> float:
    """
    Extracts the maximum salary from the salary estimate string.
    """
    if pd.isna(value):
        return None

    matches = re.findall(r"(\d+)K", value)

    if len(matches) >= 2:
        return int(matches[1]) * 1000

    return None


def extract_salary_source(value: str) -> str:
    """
    Extracts the salary estimate source.
    """
    if pd.isna(value):
        return None

    match = re.search(r"\((.+?)\)", value)

    if match:
        return match.group(1).strip()

    return None


def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """
    From 'Salary Estimate' generates four new columns:
      - Salary_Min: minimum salary in USD
      - Salary_Max: maximum salary in USD
      - Salary_Avg: average salary
      - Salary_Source: source of the estimate
    """
    if "Salary Estimate" not in df.columns:
        print("[salary]  Column 'Salary Estimate' not found")
        return df

    df["Salary_Min"] = df["Salary Estimate"].apply(extract_salary_min)
    df["Salary_Max"] = df["Salary Estimate"].apply(extract_salary_max)

    df["Salary_Avg"] = (df["Salary_Min"] + df["Salary_Max"]) / 2

    df["Salary_Source"] = df["Salary Estimate"].apply(extract_salary_source)

    # Detect rows where salary could not be parsed
    no_salary = df["Salary_Min"].isna().sum()

    if no_salary > 0:
        print(f"[salary]  {no_salary} rows without parsed salary:")
        print(df[df["Salary_Min"].isna()]["Salary Estimate"].unique())

    return df


def report(df: pd.DataFrame) -> None:
    """
    Prints quick salary statistics.
    """
    if "Salary_Min" in df.columns:
        print(
            f"\n[salary] Salary_Min — min: ${df['Salary_Min'].min():,.0f} "
            f"| max: ${df['Salary_Min'].max():,.0f}"
        )

    if "Salary_Max" in df.columns:
        print(
            f"[salary] Salary_Max — min: ${df['Salary_Max'].min():,.0f} "
            f"| max: ${df['Salary_Max'].max():,.0f}"
        )

    if "Salary_Avg" in df.columns:
        print(f"[salary] Overall average: ${df['Salary_Avg'].mean():,.0f}")

    if "Salary_Source" in df.columns:
        print("\n[salary] Estimate sources:")
        print(df["Salary_Source"].value_counts())


def save(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"[salary] Saved to: {path}")


def run(df: pd.DataFrame = None) -> pd.DataFrame:

    if df is None:
        df = pd.read_csv(INTERIM_IN)

    df = clean_salary(df)

    # Remove original column after parsing
    if "Salary Estimate" in df.columns:
        df.drop(["Salary Estimate"], axis=1, inplace=True)

    report(df)
    save(df, INTERIM_OUT)

    return df


if __name__ == "__main__":
    run()