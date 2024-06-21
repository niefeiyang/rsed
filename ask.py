from openai import OpenAI
import os
import sys
import sqlite3
from dotenv import load_dotenv
from vectordb import *

load_dotenv()
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
client = OpenAI(api_key=os.getenv("API_KEY"))
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_response TEXT
)
''')
conn.commit()

def save_message(user_message, bot_response):
    c.execute('INSERT INTO history (user_message, bot_response) VALUES (?, ?)', (user_message, bot_response))
    conn.commit()

def get_chat_history():
    c.execute('SELECT user_message, bot_response FROM history')
    return c.fetchall()

def ask(question: str):
    chroma_results = query_chromadb(question)
    chat_history = get_chat_history()
    documents = chroma_results.get('documents', [])

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    for message in chat_history:
        messages.append({"role": "user", "content": message[0]})
        messages.append({"role": "assistant", "content": message[1]})
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
    messages=messages)

    bot_response = response.choices[0].message.content
    save_message(question, bot_response)

    return bot_response

