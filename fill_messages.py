import requests

for i in range(1, 11):
    result = requests.post("http://127.0.0.1:5000/post", json={"msg": f"msg{i}"}, timeout=10)
    print(result.text)