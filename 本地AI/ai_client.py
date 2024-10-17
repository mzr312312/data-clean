# ai_client.py
from openai import OpenAI

client = OpenAI(
    api_key="sk-8H4ypTvnDgST3uNypFS3XYmmo57VOfnjGFW2pqjcG2dtLwVS",
    base_url="https://api.bianxie.ai/v1"
)

def get_models():
    models = client.models.list()
    return [model.id for model in models.data]

def generate_response(model, messages):
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content