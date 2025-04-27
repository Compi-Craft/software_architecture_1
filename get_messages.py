import requests


result = requests.get("http://127.0.0.1:5000/get", timeout=10)
print(result.text)