from twilio.rest import Client
import os
import requests
import time
from datetime import datetime

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
from_number = os.environ.get("TWILIO_FROM_NUMBER")
mailgun_api_key = os.environ.get("MAILGUN_API_KEY")
mailgun_domain = os.environ.get("MAILGUN_DOMAIN")
from_email = os.environ.get("MAILGUN_FROM_EMAIL")
email_to = os.environ.get("EMAIL_TO")

client = Client(account_sid, auth_token)

numbers = []
with open("numbers.txt", "r") as f:
    for line in f:
        number = line.strip()
        if number:
            numbers.append(number)

results = []

def map_status(s):
    return {
        "completed": "Answered",
        "busy": "Busy",
        "no-answer": "No Answer",
        "failed": "Failed",
        "canceled": "Canceled"
    }.get(s, s)

for number in numbers:
    call = client.calls.create(
        to=number,
        from_=from_number,
        url="https://twilio-webhook-server-f4lp.onrender.com/voice"
    )
    print(f"Calling {number}, SID: {call.sid}")
    while True:
        status = client.calls(call.sid).fetch().status
        if status in ["completed", "failed", "busy", "no-answer", "canceled"]:
            break
        time.sleep(2)
    results.append({"number": number, "status": map_status(status)})

csv = "Number,Status\n"
for r in results:
    csv += f"{r['number']},{r['status']}\n"

html = "<h3>Autodialer Report</h3><table border='1'><tr><th>Number</th><th>Status</th></tr>"
for r in results:
    html += f"<tr><td>{r['number']}</td><td>{r['status']}</td></tr>"
html += "</table>"

requests.post(
    f"https://api.mailgun.net/v3/sandboxe2b0fcd97379448989e4af1dfe73a656.mailgun.org/messages",
    auth=("api", mailgun_api_key),
    files={"attachment": ("report.csv", csv)},
    data={
        "from": from_email,
        "to": email_to,
        "subject": "Autodialer Report",
        "html": html
    }
)
