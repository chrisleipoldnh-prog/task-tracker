from fastapi import FastAPI

from database import engine, test_connection
from model import Base

app = FastAPI()


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Task Tracker API"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "connection": test_connection()
    }