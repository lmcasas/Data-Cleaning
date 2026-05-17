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


import pandas as pd
import re

TITLE_RULES = {
    "Data Scientist": ["data scientist"],
    "Machine Learning Engineer": [
        "machine learning engineer", 
        "ml engineer",
        r"ml.*engineer", 
        r"machine learning.*engineer"
    ],
    "Machine Learning Scientist": [
        "machine learning scientist", 
        "ml scientist",
        r"ml.*scientist",
        r"machine learning.*scientist"
    ],
    "Data Engineer": ["data engineer"],
    "Data Analyst": [
        "data analyst", 
        "business data analyst", 
        "bi analyst",
        r"bi.*analyst",
        "business intelligence analyst"
    ],
    "Business Intelligence Analyst": ["business intelligence"],
    "Analytics Manager": ["analytics manager"],
    "Software Engineer (Data)": [
        r"software engineer.*data",
        r"data.*software engineer"
    ],
    "Research Scientist": ["research scientist"],
}

def categorize_title(cleaned_title: str) -> str:
    if pd.isna(cleaned_title) or cleaned_title == "":
        return "Other"
    
    title_lower = cleaned_title.lower().strip()
    
    for category, patterns in TITLE_RULES.items():
        for pattern in patterns:
            if isinstance(pattern, str) and pattern.startswith('r\\'):
                pattern_clean = pattern[2:]  
                if re.search(pattern_clean, title_lower):
                    return category
            elif pattern in title_lower:
                if category == "Data Scientist" and "data scientist" in title_lower:
                    if not any(x in title_lower for x in ['machine', 'research']):
                        return category
                else:
                    return category
    
    if "scientist" in title_lower:
        excluded_terms = ['data', 'research', 'machine learning', 'ml']
        if not any(term in title_lower for term in excluded_terms):
            return "Scientist (Other)"
    
    return "Other"


SENIOR_WORDS = {"sr", "senior", "lead", "principal", "staff"}
JUNIOR_WORDS = {"jr", "junior", "associate"}


def extract_level(title: str) -> str:
    """
    Extract seniority level from the job title.
    """
    if pd.isna(title):
        return "Unknown"

    words = set(title.split())

    if words & SENIOR_WORDS:
        return "Senior"

    if words & JUNIOR_WORDS:
        return "Junior"

    return "Mid"


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