# Data Cleaning Pipeline — DS Jobs

This project implements a data cleaning pipeline for Data Science job postings. The pipeline processes raw data and applies sequential transformations to generate a clean and structured dataset.

## Pipeline Steps

The pipeline consists of 7 steps executed in order:

- **00 — Ingest**: Loads raw data from the `data/raw/` directory
- **01 — Job Title**: Cleans and standardizes job titles
- **02 — Company Name**: Normalizes company names
- **03 — Salary Estimate**: Processes and standardizes salary estimates
- **04 — Job Description**: Cleans and processes job descriptions
- **05 — Company Info**: Extracts and normalizes company information
- **06 — Validate + Export**: Validates data and exports the clean dataset

## Project Structure

```
.
├── main.py              # Main script that runs the pipeline
├── src/                 # Pipeline step modules
│   ├── ingest.py
│   ├── job_title.py
│   ├── company_name.py
│   ├── salary.py
│   ├── job_description.py
│   ├── company_info.py
│   └── validate.py
├── data/                # Data directory
│   ├── raw/            # Raw input data
│   ├── interim/        # Intermediate pipeline data
│   └── processed/      # Final processed data
└── notebooks/          # Analysis notebooks
```

## Usage

To run the complete pipeline:

```bash
python main.py
```

The pipeline will generate the clean file at:
```
data/processed/DS_jobs_clean.csv
```

## Requirements

- Python 3.x
- Pandas

## Output

The pipeline produces a clean dataset with the following characteristics:
- Standardized job titles
- Normalized company names
- Processed salary estimates
- Clean descriptions
- Structured company information
- Data quality validation
