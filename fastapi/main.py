from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import os

from repo_clone import *
from vectordb import *
from ask import *

print("e")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class StoreRequest(BaseModel):
    repolink: str

class AskRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/api/store_repo")
async def store_repo(store_request: StoreRequest):
    repo_path = repo_clone(store_request.repolink)
    if store_request.repolink:
        split_and_store_files(repo_path)
    return {"result": "success"}

@app.post("/api/ask")
async def ask_def(ask_request: AskRequest):
        result = ask(ask_request.question)
        return {"answer": result}




