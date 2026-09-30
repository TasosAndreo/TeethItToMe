from fastapi import FastAPI, UploadFile, File

from pathlib import Path

# Directory where uploaded audio files will be stored
UPLOAD_DIR = Path("uploads")

# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Greek Medical ASR Backend is running!"
    }

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    # Create the path where the file will be saved
    file_path = UPLOAD_DIR / file.filename

    # Read the uploaded file
    audio_data = await file.read()

    # Save the audio file
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_data)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(audio_data),
        "saved_to": str(file_path)
    }