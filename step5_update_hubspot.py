import requests
from config import HEADERS, HS_DATE_PROPERTY
from config import HEADERS, LIST_ID, SEGMENT_NAME, HS_DATE_PROPERTY


def run(contact_updates):
    """
    Sends batch-update requests to HubSpot in groups of 100.
    Raises an exception if any batch fails.
    """
    url = "https://api.hubapi.com/crm/v3/objects/contacts/batch/update"
    total_batches = (len(contact_updates) + 99) // 100

    print(f"  Sending {len(contact_updates)} updates in {total_batches} batch")

    for i in range(0, len(contact_updates), 100):
        batch = contact_updates[i:i + 100]
        batch_num = (i // 100) + 1
        payload = {"inputs": batch}

        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code in [200, 201, 202]:
            print(f"  Batch {batch_num}/{total_batches}: updated {len(batch)} contacts.")
        else:
            raise RuntimeError(
                f"Batch {batch_num}/{total_batches} failed — "
                f"HTTP {response.status_code}: {response.text}"
            )

    print(f"  All {len(contact_updates)} contacts updated successfully.")
