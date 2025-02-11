from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Header, Request

app = FastAPI()

@app.get("/")
def index():
    return "Hello World"

@app.get("/now")
def now():
	return datetime.utcnow().strftime("%Y-%m-%d, %H:%M:%S.%f")

@app.get("/user-agent")
def user_agent(user_agent: Annotated[str | None, Header()] = None):
	return user_agent

@app.get("/request")
def request_info(request: Request):
	return f'Request method: {request.method} url: {request.url} Headers: {request.headers}'

