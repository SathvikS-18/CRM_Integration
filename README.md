# CRM_Integration

A Python pipeline that reads the latest login data from an Excel file and updates a custom property (`TRE LAST USED INTERNAL`) for contacts in a specific HubSpot segment.

---

## Folder Structure

```
pipeline/
├── config.py                      # Shared configuration (token, file path, list ID, property name)
├── step1_load_excel.py            # Step 1 — Load the Excel file and build email → date lookup
├── step2_get_segment_members.py   # Step 2 — Fetch contact IDs from the HubSpot segment
├── step3_read_contact_emails.py   # Step 3 — Batch-read contact emails from HubSpot
├── step4_match_contacts.py        # Step 4 — Match segment contacts against the Excel data
├── step5_update_hubspot.py        # Step 5 — Push property updates to HubSpot in batches
├── HubSpot_Pipeline.py            # Main orchestrator — runs all steps in order

```

---

## Prerequisites

### Python Version
Python 3.9 or higher.

### Virtual Environment
A virtual environment named `pipeline` is included. Activate it before running:

```powershell
& "~\pipeline\Scripts\Activate.ps1"
```

### Required Packages
Install dependencies inside the virtual environment:

```powershell
pip install pandas requests openpyxl
```

---

## Configuration

Open `config.py` and update the following values:

| Variable | Description |
|---|---|
| `HUBSPOT_TOKEN` | Your HubSpot Private App access token |
| `FILE_PATH` | Absolute path to the Excel input file |
| `HS_DATE_PROPERTY` | Internal name of the HubSpot property to update |
| `SEGMENT_NAME` | Display name of the HubSpot segment (for logging only) |
| `LIST_ID` | Numeric ID of the HubSpot segment (found in the list URL) |

**Finding the List ID:**  
Go to HubSpot → Contacts → Lists → open your segment.  
The ID is in the URL: `.../objectLists/1111/...` → List ID is `1111`.

---

## Excel File Format

The input Excel file must contain at least the following columns (case-sensitive):

| Column | Description |
|---|---|
| `email` | Contact's email address |
| `last_access_date` | The date value to push to HubSpot |

- Each worksheet should be named with a date (e.g. `2026_Apr_02`).
- The pipeline automatically picks the **most recent sheet** based on the sheet name.

---

## Running the Pipeline

```powershell
cd "~\pipeline"
python Pipeline.py
```

### Expected Output

```
============================================================
  HubSpot Segment Update Pipeline
============================================================

[Step 1 - Load Excel] Starting...
  Reading worksheet: '2026_Apr_02'
  Loaded 150 rows from Excel.
[Step 1 - Load Excel] Completed.

[Step 2 - Get Segment Members] Starting...
  Found 20 contacts in the segment.
[Step 2 - Get Segment Members] Completed.

[Step 3 - Read Contact Emails] Starting...
  Retrieved details for 20 contacts.
[Step 3 - Read Contact Emails] Completed.

[Step 4 - Match Contacts] Starting...
  20 contacts matched and ready to update.
[Step 4 - Match Contacts] Completed.

[Step 5 - Update HubSpot] Starting...
  Batch 1/1: updated 20 contacts.
[Step 5 - Update HubSpot] Completed.

============================================================
  Pipeline completed successfully.
============================================================
```

---

## Error Handling

If any step fails, the pipeline stops immediately and reports which step failed, the reason, and a full traceback. Example:

```
[Step 2 - Get Segment Members] FAILED — pipeline stopped.
  Reason: HubSpot API error 401: ...

--- Traceback ---
...
```

Common errors:

| Error | Cause | Fix |
|---|---|---|
| `FileNotFoundError` | Excel file not found at `FILE_PATH` | Update `FILE_PATH` in `config.py` |
| `KeyError: 'email'` | Column name mismatch in Excel | Ensure the column is named `email` (lowercase) |
| `HTTP 401` | Invalid HubSpot token | Update `HUBSPOT_TOKEN` in `config.py` |
| `HTTP 404` | Wrong `LIST_ID` | Verify the list ID from the HubSpot URL |
| `No contacts matched` | Emails in segment not found in Excel | Check that the Excel sheet has the correct email addresses |
