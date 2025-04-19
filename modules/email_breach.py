import time

# Fake breach data for demo/testing
KNOWN_BREACHED_EMAILS = {
    "test@example.com": ["LinkedIn 2012", "Adobe 2013"],
    "hacker123@gmail.com": ["Collection #1", "MyFitnessPal 2018"]
}

def check_email_breach(email):
    print(f"[*] Checking email breach status for: {email}")
    time.sleep(1)  # Simulate a delay
    breaches = KNOWN_BREACHED_EMAILS.get(email.lower(), [])
    return breaches
