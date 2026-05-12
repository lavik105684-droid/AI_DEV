import requests
try:
    r = requests.get("http://localhost:8501/?agent=Manager&status=Working&message=TestFromScript")
    print(f"Status Code: {r.status_code}")
except Exception as e:
    print(f"Error: {e}")
