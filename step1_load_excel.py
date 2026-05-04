import pandas as pd
import os
from config import FILE_PATH
import openpyxl


def run():
    """
    Loads the latest sheet from the Excel file.
    Returns a dict mapping lowercase email -> login date string.
    Raises an exception if the file is missing or unreadable.
    """
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"Excel file not found at: {FILE_PATH}")

    xl = pd.ExcelFile(FILE_PATH)
    sheets = xl.sheet_names

    try:
        # Sheet names use underscores (e.g. '2026_Apr_02') — replace with spaces for parsing
        normalized = [s.replace('_', ' ') for s in sheets]
        sheet_dates = pd.to_datetime(normalized, errors='coerce')
        latest_index = sheet_dates.dropna().argmax()
        latest_sheet = sheets[latest_index]
    except Exception:
        latest_sheet = sorted(sheets)[-1]

    print(f"  Reading worksheet: '{latest_sheet}'")
    df = pd.read_excel(FILE_PATH, sheet_name=latest_sheet)

    excel_lookup = {}
    for _, row in df.iterrows():
        email = str(row['email']).strip().lower()
        last_used = str(row['last_access_date']).strip()
        excel_lookup[email] = last_used

    if not excel_lookup:
        raise ValueError("Excel file loaded but no rows were found.")

    print(f"  Loaded {len(excel_lookup)} rows from Excel.")
    return excel_lookup
