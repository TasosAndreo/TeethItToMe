from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Greek Medical ASR Backend is running!"
    }