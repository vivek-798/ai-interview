from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import run_interview

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/start-interview")
def start_interview():
    result = run_interview()
    return result
