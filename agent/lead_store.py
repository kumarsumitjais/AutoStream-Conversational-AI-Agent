import json
from datetime import datetime
from pathlib import Path


LEADS_FILE = Path("data/leads.json")


def save_lead(name: str, email: str, platform: str, plan: str):
    """Save a new lead with timestamp"""
    now = datetime.now().isoformat()

    lead = {
        "name": name,
        "email": email,
        "platform": platform,
        "interested_plan": plan,
        "created_at": now,
        "last_contacted_at": now,
        "reinterest_count": 0
    }

    if LEADS_FILE.exists():
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(lead)

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)



def lead_exists(email: str) -> bool:
    """Check if a lead with the same email already exists"""
    if not LEADS_FILE.exists():
        return False

    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        leads = json.load(f)

    email = email.lower().strip()
    return any(lead.get("email", "").lower() == email for lead in leads)



def update_existing_lead(email: str, new_plan: str = None):
    """Update timestamp when an existing lead shows interest again"""
    if not LEADS_FILE.exists():
        return

    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        leads = json.load(f)

    for lead in leads:
        if lead.get("email", "").lower() == email.lower():
            lead["last_contacted_at"] = datetime.now().isoformat()
            lead["reinterest_count"] = lead.get("reinterest_count", 0) + 1

            if new_plan:
                lead["interested_plan"] = new_plan
            break

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=4)
