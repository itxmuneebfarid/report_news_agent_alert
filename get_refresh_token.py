from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Use your current installed credentials file
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

# Save in authorized_user format
data = {
    "client_id": creds.client_id,
    "client_secret": creds.client_secret,
    "refresh_token": creds.refresh_token,
    "type": "authorized_user"
}

with open("credentials.json", "w") as f:
    json.dump(data, f, indent=4)

print("✅ credentials.json updated with refresh_token")
