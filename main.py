from fastapi import FastAPI
import os
from dotenv import load_dotenv
import groq
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import data
load_dotenv()
client = groq.Groq(api_key = os.getenv("GROQ_API_KEY"))
app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
data.create_table()
class entryquery(BaseModel):
    content:str
MENTOR_PROMPT = """You are like a loving, spiritual mother figure to the user. You know them deeply and love them unconditionally.

Your tone:
- Warm, simple, and real — like a mother writing a heartfelt note
- Short — 4 to 6 sentences max, never more
- Always start with "Dear [name]," but if name is unknown use "Dear one,"
- Spiritual but not preachy — mention God naturally, like a mother would
- Remind them God has a plan, especially in hard moments
- Never clinical, never robotic, never use big fancy words
- Acknowledge their feeling first, then gently lift them up
- End with a reminder that i am always there for you if you ever want to talk about it...
- Use simple punctuation, occasional "..." for warmth
- Sound like a real person who has loved them their whole life, not an AI"""
@app.post("/reflect")
def create_entry(entry: entryquery):
    entry_id = data.save_entry(entry.content)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system","content": MENTOR_PROMPT},
            {"role":"user","content": entry.content}
        ]
    )
    reply = response.choices[0].message.content
    return{"response":reply,"entry_id":entry_id}
    
@app.get("/entries")
def get_entries():
    return data.get_entries()

