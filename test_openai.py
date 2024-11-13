import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("Error: La clave de API de OpenAI no está configurada.")
    exit(1)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OPENAI_API_KEY}',
}

data = {
    'model': 'gpt-3.5-turbo',
    'messages': [
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola, ¿cómo estás?"}
    ],
    'max_tokens': 50,
    'temperature': 0.7,
}

response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print("Respuesta de OpenAI:")
    print(result['choices'][0]['message']['content'].strip())
else:
    print(f"Error {response.status_code}: {response.text}")