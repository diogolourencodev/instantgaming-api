import requests

url = "http://127.0.0.1:5000/api/search/elden%20ring?platform=steam&type=games-and-dlc"
resp = requests.get(url, timeout=30)
resp.raise_for_status()
print(resp.json())
