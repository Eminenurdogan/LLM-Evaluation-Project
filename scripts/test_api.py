
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Proje ana klasorundeki .env dosyasini oku
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("API Key bulunamadi! .env dosyasini kontrol et.")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "qwen/qwen3.7-flash",
    "messages": [
        {
            "role": "user",
            "content": "Merhaba! Kendini kisaca tanit."
        }
    ],
    "max_tokens": 80
}

response = None 

try:
    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    print("\nAPI BAGLANTISI BASARILI!")
    print("AI Cevabi:", result["choices"][0]["message"]["content"])

except requests.exceptions.RequestException as error:
    print("API HATASI:", error)
    if response is not None:
        print(response.text)
