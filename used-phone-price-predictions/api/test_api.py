import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "features": [12, 4, 64, 6, 3000, 1, 0, 2]  # 8 FEATURES
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)