import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

models = client.models.list()

for model in models:
    print(model.name)
