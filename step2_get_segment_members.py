import requests
from config import HEADERS, LIST_ID, SEGMENT_NAME, HS_DATE_PROPERTY


def run():
    """
    Fetches all contact IDs that are members of the HubSpot segment.
    Returns a list of contact ID strings.
    Raises an exception if the API call fails.
    """
    print(f"  Fetching members of '{SEGMENT_NAME}' (List ID: {LIST_ID})")

    url = f"https://api.hubapi.com/crm/v3/lists/{LIST_ID}/memberships/join-order"
    response = requests.get(url, headers=HEADERS, params={"limit": 100})

    if response.status_code != 200:
        raise RuntimeError(
            f"HubSpot API error {response.status_code}: {response.text}"
        )

    member_records = response.json().get("results", [])
    contact_ids = [str(m["recordId"]) for m in member_records]

    if not contact_ids:
        raise ValueError(f"Segment '{SEGMENT_NAME}' (List ID: {LIST_ID}) returned 0 members.")

    print(f"  Found {len(contact_ids)} contacts in the segment.")
    return contact_ids
