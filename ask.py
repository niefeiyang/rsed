from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY"))
from dotenv import load_dotenv
from vectordb import *
load_dotenv()


def ask(question: str):
    chroma_results = query_chromadb(question)

    documents = chroma_results.get('documents', [])
    ids = chroma_results.get('ids', [])

    system_message="You are a helpful assistant."
    user_message=f"Given the following documents: {documents} with IDs: {ids}, answer the following question with document itself and details, and please also tell me its ids: {question}"

    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ])

    return response.choices[0].message.content.strip()


