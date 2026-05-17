import sys
import time

from src import ingest          as step_00
from src import job_title       as step_01
from src import company_name    as step_02
from src import salary          as step_03
from src import job_description as step_04
from src import company_info    as step_05
from src import validate        as step_06


FINAL_OUTPUT = "data/processed/DS_jobs_clean.csv"


# Pipeline
STEPS = [
    ("00 — Ingest",            step_00, False),
    ("01 — Job Title",         step_01, True),
    ("02 — Company Name",      step_02, True),
    ("03 — Salary Estimate",   step_03, True),
    ("04 — Job Description",   step_04, True),
    ("05 — Company Info",      step_05, True),
    ("06 — Validate + Export", step_06, True),
]


def run():
    """
    Runs the full data cleaning pipeline step by step.
    """
    print("=" * 55)
    print("  DATA CLEANING PIPELINE — DS Jobs")
    print("=" * 55)

    df = None
    total_start = time.time()

    for name, step, needs_df in STEPS:

        print(f"\n▶ {name}")
        print("-" * 40)

        start = time.time()

        try:
            if needs_df:
                df = step.run(df)
            else:
                df = step.run()

        except Exception as e:
            print(f"\n[pipeline] Error in step '{name}'")
            print(f"[pipeline] {type(e).__name__}: {e}")
            sys.exit(1)

        elapsed = time.time() - start
        rows = len(df) if df is not None else "?"

        print(f" Complete in {elapsed:.2f}s — {rows} rows")

    total = time.time() - total_start

    print("\n" + "=" * 55)
    print(f"  Pipeline complete in {total:.2f}s")
    print(f"  Output: {FINAL_OUTPUT}")
    print("=" * 55)


if __name__ == "__main__":
    run()