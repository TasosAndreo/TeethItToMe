import shutil

from fastapi import FastAPI, UploadFile, File

from pathlib import Path

from faster_whisper import WhisperModel

from medical_terms.dentistry_corrections import correct_dental_word

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

initial_prompt = f"""
Ελληνική οδοντιατρική ιατρική ορολογία.
Χρησιμοποιούνται οι ακόλουθοι όροι:
{DENTISTRY_TERMS}
"""

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

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    segments, info = model.transcribe(
        str(file_path),
        language="el",
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=True,
        initial_prompt=initial_prompt,
        word_timestamps=True
    )

    corrected_transcription = ""

    for segment in segments:

        if segment.words:

            for i, word in enumerate(segment.words):

                previous_words = [
                    w.word.strip(" ,.!;:")
                    for w in segment.words[max(0, i - 2):i]
                ]

                next_words = [
                    w.word.strip(" ,.!;:")
                    for w in segment.words[i + 1:i + 3]
                ]

                original_word = word.word

                corrected_word = correct_dental_word(
                    original_word,
                    previous_words,
                    next_words
                )

                # Preserve whitespace/punctuation from Whisper
                leading_spaces = len(original_word) - len(original_word.lstrip())
                trailing_spaces = len(original_word) - len(original_word.rstrip())

                prefix = original_word[:leading_spaces]
                suffix = original_word[len(original_word) - trailing_spaces:] if trailing_spaces > 0 else ""

                corrected_transcription += (
                    prefix
                    + corrected_word.strip(" ,.!;:")
                    + suffix
                )

        else:
            corrected_transcription += segment.text


    return corrected_transcription.strip()