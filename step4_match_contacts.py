from config import HS_DATE_PROPERTY
from config import HEADERS, LIST_ID, SEGMENT_NAME

def run(segment_contacts, excel_lookup):
    """
    Matches segment contacts against the Excel lookup by email.
    Returns a list of HubSpot batch-update input dicts.
    Raises an exception if no contacts match.
    """
    contact_updates = []
    skipped = []

    for contact in segment_contacts:
        contact_id = contact.get("id")
        email = (contact.get("properties", {}).get("email") or "").strip().lower()

        if email in excel_lookup:
            contact_updates.append({
                "id": contact_id,
                "properties": {
                    HS_DATE_PROPERTY: excel_lookup[email]
                }
            })
        else:
            skipped.append(email or f"ID:{contact_id}")

    if skipped:
        print(f"  Skipped {len(skipped)} contacts not found in Excel:")
        for s in skipped:
            print(f"    - {s}")

    if not contact_updates:
        raise ValueError(
            "No contacts from the segment matched any email in the Excel file. Nothing to update."
        )

    print(f"  {len(contact_updates)} contacts matched and ready to update.")
    return contact_updates
