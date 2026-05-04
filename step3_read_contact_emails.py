import requests
from config import HEADERS
from config import HEADERS, LIST_ID, SEGMENT_NAME, HS_DATE_PROPERTY


def run(contact_ids):
    """
    Batch-reads email, firstname, and lastname for a list of contact IDs.
    Returns a list of HubSpot contact result objects.
    Raises an exception if the API call fails.
    """
    print(f"  Batch-reading contact details for {len(contact_ids)} contacts")

    url = "https://api.hubapi.com/crm/v3/objects/contacts/batch/read"
    payload = {
        "inputs": [{"id": cid} for cid in contact_ids],
        "properties": ["email", "firstname", "lastname"]
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code not in [200, 207]:
        raise RuntimeError(
            f"HubSpot API error {response.status_code}: {response.text}"
        )

    contacts = response.json().get("results", [])
    print(f"  Retrieved details for {len(contacts)} contacts.")
    return contacts
