from fastapi import FastAPI, UploadFile, File

from pathlib import Path

from faster_whisper import WhisperModel

app = FastAPI()

# Directory where uploaded audio files will be stored
UPLOAD_DIR = Path("uploads")

# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)

# WHISPER MODEL
model = WhisperModel("small", device="cpu",compute_type="int8")

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

     # WHISPER TRANSCRIPTION
    segments, info = model.transcribe(str(file_path),language="el")

    # Combine all Whisper segments
    transcription = ""
    for segment in segments:transcription += segment.text

    return {
        "filename": file.filename,
        "language": info.language,
        "language_probability": info.language_probability,
        "text": transcription
    }