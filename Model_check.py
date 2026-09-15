import requests

GEMINI_API_KEY = "your API"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"

res = requests.get(url).json()
for model in res.get('models', []):
    if "generateContent" in model.get('supportedGenerationMethods', []):
        # In ra tên model có thể dùng
        print(model['name'].replace("models/", ""))