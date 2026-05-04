import sys
import traceback

import step1_load_excel
import step2_get_segment_members
import step3_read_contact_emails
import step4_match_contacts
import step5_update_hubspot


# Pipeline definition — each entry is (step_name, callable, *args_from_ctx)
# Steps run in order. If any step crashes, the pipeline stops immediately.


def run_step(step_name, func, *args):
    """Runs a single pipeline step. Returns the result or exits on failure."""
    print(f"\n[{step_name}] STARTING")
    try:
        result = func(*args)
        print(f"[{step_name}] COMPLETED SUCCESSFULLY.")
        return result
    except Exception as e:
        print(f"\n[{step_name}] FAILED — pipeline stopped.")
        print(f"  Reason: {e}")
        print("\n--- Traceback ---")
        traceback.print_exc()
        sys.exit(1)


print("=" * 60)
print("  HubSpot Segment Update Pipeline")
print("=" * 60)

# Step 1: Load Excel and build email to last-used-date lookup
excel_lookup = run_step(
    "Step 1 - Load Excel",
    step1_load_excel.run
)

# Step 2: Get contact IDs from the HubSpot segment
contact_ids = run_step(
    "Step 2 - Get Segment Members",
    step2_get_segment_members.run
)

# Step 3: Batch-read email addresses for those contact IDs
segment_contacts = run_step(
    "Step 3 - Read Contact Emails",
    step3_read_contact_emails.run,
    contact_ids
)

# Step 4: Match segment contacts against Excel 
contact_updates = run_step(
    "Step 4 - Match Contacts",
    step4_match_contacts.run,
    segment_contacts,
    excel_lookup
)

# Step 5: Push updates to HubSpot
run_step(
    "Step 5 - Update HubSpot",
    step5_update_hubspot.run,
    contact_updates
)

print("\n" + "=" * 60)
print("  Pipeline completed successfully.")
print("=" * 60)
