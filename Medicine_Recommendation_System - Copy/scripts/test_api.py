import requests
import json

# Flask server run cheyyunna URL
url = 'http://127.0.0.1:5000/predict'

# Frontend-il ninnu varunnathu pole kurachu sample symptoms kodukkunnu
data = {
    "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]
}

print("Sending request to API...")

# API-lekku POST request ayakkunnu
response = requests.post(url, json=data)

# Kittiya Result print cheyyunnu
print("\n--- Prediction Result ---")
print(json.dumps(response.json(), indent=4))