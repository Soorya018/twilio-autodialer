
---


```markdown
# Twilio Autodialer

This repository contains the Python script that initiates phone calls using Twilio and generates daily reports of call statuses.  
It integrates with **Mailgun** to send email reports.

---

##  Overview

- Reads a list of phone numbers from `numbers.txt`.  
- Uses **Twilio’s Python SDK** to call Twilio’s REST API and initiate outbound calls.  
- For each call, waits until the final status (`completed`, `failed`, `busy`, etc.) is available.  
- Builds a **CSV + HTML report** summarizing the calls.  
- Sends the report via **Mailgun** as an email.

---

##  File Structure

- **autodialer.py** → Main Python script that initiates calls, checks statuses, and sends email report.  
- **numbers.txt** → List of phone numbers to call (E.164 format, e.g., `+353894117081`).  
- **requirements.txt** → Dependencies (`twilio`, `requests`).  
- **.github/workflows/autodialer.yml** → GitHub Actions workflow to schedule the script daily.  

---

##  Flow

1. **Read Numbers**  
   Numbers are read from `numbers.txt`.

2. **Place Calls via Twilio SDK**  
   Each number is called using:  
   ```python
   client.calls.create(
       to=number,
       from_=from_number,
       url="https://<your-webhook-server>/voice"
   )
