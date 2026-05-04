# --- SHARED CONFIGURATION ---
# Edit these values before running the pipeline.

HUBSPOT_TOKEN = "access_token"

FILE_PATH = r"user_last_login_tre.xlsx"

HS_DATE_PROPERTY = "TRE LAST USED INTERNAL"  # Internal HubSpot property name

SEGMENT_NAME = "List of Active Users"
LIST_ID = 1111  # From: https://app-eu1.hubspot.com/contacts/139630575/objectLists/xxxx/

HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}
