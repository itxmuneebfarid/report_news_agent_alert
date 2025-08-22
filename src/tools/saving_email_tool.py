import csv
import os

EMAIL_FILE = "emails.csv"

def save_email_to_csv(email: str):
    """Save a new email into emails.csv """
    file_exists = os.path.exists(EMAIL_FILE)

    with open(EMAIL_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email"])
        if not file_exists:  
            writer.writeheader()

        emails = load_emails_from_csv()
        if email not in emails:
            writer.writerow({"email": email})


def load_emails_from_csv():
    """Load all saved emails"""
    if not os.path.exists(EMAIL_FILE):
        return []

    with open(EMAIL_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return [row["email"] for row in reader if "email" in row]
