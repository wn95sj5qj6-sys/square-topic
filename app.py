from fastapi import FastAPI
from topic_main import run_topic

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "service running"}

@app.get("/run")
def run():
    result = run_topic()
    if not result:
        return {"error": "no result"}
    return result
