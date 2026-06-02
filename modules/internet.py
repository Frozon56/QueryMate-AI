import requests

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False