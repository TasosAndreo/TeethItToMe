from fastapi import FastAPI, UploadFile, File

from pathlib import Path

from faster_whisper import WhisperModel

app = FastAPI()

# Directory where uploaded audio files will be stored
UPLOAD_DIR = Path("uploads")

# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)

MEDICAL_TERMS_DIR = Path("medical_terms")
DENTISTRY_TERMS_FILE = MEDICAL_TERMS_DIR / "dentistry.txt"

# Load medical vocabulary
def load_terms(file_path: Path) -> str:
    if not file_path.exists():
        return ""

    terms = [
        line.strip()
        for line in file_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    return ", ".join(terms)

DENTISTRY_TERMS = load_terms(DENTISTRY_TERMS_FILE)

# Whisaper model
model = WhisperModel("small", device="cpu",compute_type="int8")

@app.get("/")
def home():
    return {
        "message": "Greek Medical ASR Backend is running!"
    }

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    audio_data = await file.read()

    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_data)

    initial_prompt = f"""
    Ελληνική οδοντιατρική ιατρική ορολογία.
    Χρησιμοποιούνται οι ακόλουθοι όροι:
    {DENTISTRY_TERMS}
    """

    segments, info = model.transcribe(
        str(file_path),
        language="el",
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=True,
        initial_prompt=initial_prompt,
        word_timestamps=True
    )

    transcription = ""
    timestamped_segments = []

    for segment in segments:
        transcription += segment.text

        words = []

        if segment.words:
            for word in segment.words:
                words.append({
                    "start": word.start,
                    "end": word.end,
                    "word": word.word
                })

        timestamped_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
            "words": words
     })

    return {
        "filename": file.filename,
        "language": info.language,
        "language_probability": info.language_probability,
        "text": transcription,
        "segments": timestamped_segments
    }