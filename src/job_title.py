import pandas as pd
import re

INTERIM_IN = "data/interim/01_after_ingest.csv"
INTERIM_OUT = "data/interim/02_after_job_title.csv"


def clean_title(title: str) -> str:
    """
    Normalize job titles for easier matching.
    """
    if pd.isna(title):
        return None

    title = title.lower()
    title = re.sub(r"[^\w\s]", " ", title)
    title = re.sub(r"\s+", " ", title)

    return title.strip()

TITLE_RULES = {
    "Data Scientist": [
        r"\bdata scientist\b"
    ],
    "Machine Learning Engineer": [
        r"\bmachine learning engineer\b",
        r"\bml engineer\b",
        r"\bml.*engineer\b",
        r"\bmachine learning.*engineer\b"
    ],
    "Machine Learning Scientist": [
        r"\bmachine learning scientist\b",
        r"\bml scientist\b",
        r"\bml.*scientist\b",
        r"\bmachine learning.*scientist\b"
    ],
    "Data Engineer": [
        r"\bdata engineer\b"
    ],
    "Data Analyst": [
        r"\bdata analyst\b",
        r"\bbusiness data analyst\b",
        r"\bbi analyst\b",
        r"\bbi.*analyst\b",
        r"\bbusiness intelligence analyst\b"
    ],
    "Business Intelligence Analyst": [
        r"\bbusiness intelligence\b"
    ],
    "Analytics Manager": [
        r"\banalytics manager\b"
    ],
    "Software Engineer (Data)": [
        r"\bsoftware engineer.*data\b",
        r"\bdata.*software engineer\b"
    ],
    "Research Scientist": [
        r"\bresearch scientist\b"
    ],
}


def categorize_title(cleaned_title: str) -> str:
    if pd.isna(cleaned_title) or cleaned_title == "":
        return "Other"
    
    title_lower = cleaned_title.lower().strip()
    
    for category, patterns in TITLE_RULES.items():
        for pattern in patterns:
            if re.search(pattern, title_lower):
                if category == "Data Scientist":
                    if any(term in title_lower for term in ["machine", "research"]):
                        continue

                return category

    if "scientist" in title_lower:
        excluded_terms = ["data", "research", "machine learning", "ml"]

        if not any(term in title_lower for term in excluded_terms):
            return "Scientist (Other)"
    
    return "Other"


SENIOR_WORDS = {"sr", "senior", "lead", "principal", "staff"}
JUNIOR_WORDS = {"jr", "junior", "associate"}


def extract_level(title: str) -> str:
    """
    Extract seniority level from the job title.
    """
    if pd.isna(title) or title == "":
        return "Unknown"

    words = set(title.lower().split())

    if words & SENIOR_WORDS:
        return "Senior"

    if words & JUNIOR_WORDS:
        return "Junior"

    return "Unknown"


def clean_job_title(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all job title transformations.
    """
    if "Job Title" not in df.columns:
        print("[job_title]  Column 'Job Title' not found")
        return df

    df["Title"] = df["Job Title"].apply(clean_title)
    df["Job_category"] = df["Title"].apply(categorize_title)
    df["Level"] = df["Title"].apply(extract_level)

    return df


def report(df: pd.DataFrame) -> None:
    """
    Print quick diagnostics about the transformation.
    """
    if "Job_category" in df.columns:
        print("\n[job_title] Categories found:")
        print(df["Job_category"].value_counts())

    if "Level" in df.columns:
        print("\n[job_title] Levels found:")
        print(df["Level"].value_counts())

    if "Title" in df.columns:
        print("\n[job_title] Unique cleaned titles:")
        print(df["Title"].unique())


def save(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"[job_title] Saved to: {path}")


def run(df: pd.DataFrame | None = None) -> pd.DataFrame:
    
    if df is None:
        df = pd.read_csv(INTERIM_IN)

    df = clean_job_title(df)
    report(df)
    save(df, INTERIM_OUT)

    return df


if __name__ == "__main__":
    run()