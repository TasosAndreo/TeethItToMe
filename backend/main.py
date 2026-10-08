import shutil
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from pydantic import BaseModel
from faster_whisper import WhisperModel
from medical_terms.dentistry_corrections import correct_dental_word

# Directories for recordings and their transcriptions
RECORDINGS_DIR = Path("recordings")
UPLOAD_DIR = RECORDINGS_DIR / "audio"
TRANSCRIPT_DIR = RECORDINGS_DIR / "transcripts"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

MEDICAL_TERMS_DIR = Path("medical_terms")
DENTISTRY_TERMS_FILE = MEDICAL_TERMS_DIR / "dentistry.txt"

app = FastAPI()

class TranscriptUpdate(BaseModel):
    text: str

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
model = WhisperModel("medium",
                      device="cpu",
                      compute_type="int8")

@app.get("/")
def home():
    return {
        "message": "Greek Medical ASR Backend is running!"
    }

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    # Set a unique ID for the recording based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Keep the original audio extension, such as .wav or .mp3
    original_filename = Path(file.filename or "recording.wav")
    extension = original_filename.suffix.lower() or ".wav"

    # Use the same ID for the audio and transcript
    recording_name = f"recording_{timestamp}"
    audio_path = UPLOAD_DIR / f"recording_{timestamp}{extension}"
    transcript_path = TRANSCRIPT_DIR / f"{recording_name}.txt"

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    segments, info = model.transcribe(
        str(audio_path),
        language="el",
        beam_size=5,
        vad_filter=False,
        condition_on_previous_text=True,
        initial_prompt=initial_prompt,
        word_timestamps=True
    )

    corrected_transcription = ""
    
    segment_count = 0
    last_segment_end = 0.0

    for segment in segments:

        segment_count += 1
        last_segment_end = segment.end

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

    # Prepare the final corrected text
    corrected_transcription = corrected_transcription.strip()

    # Save the transcription as UTF-8 to preserve Greek characters
    transcript_path.write_text(
        corrected_transcription,
        encoding="utf-8"
    )

    print(f"Segments processed: {segment_count}")
    print(f"Last segment ends at: {last_segment_end:.2f} seconds")
    print(f"Audio saved: {audio_path}")
    print(f"Transcript saved: {transcript_path}")

    # Return plain text to the frontend
    return corrected_transcription

@app.get("/recordings")
def get_recordings():

    recordings = []

    for audio_file in sorted(UPLOAD_DIR.iterdir(), reverse=True):

        if not audio_file.is_file():
            continue

        transcript_file = TRANSCRIPT_DIR / f"{audio_file.stem}.txt"

        recordings.append({
            "name": audio_file.stem,
            "audio": audio_file.name,
            "transcript": transcript_file.name 
            if transcript_file.exists() 
            else None
        })

    return recordings

@app.get(
    "/recordings/{recording_name}/transcript",
    response_class=PlainTextResponse
)
def get_transcript(recording_name: str):

    transcript_path = TRANSCRIPT_DIR / f"{recording_name}.txt"

    if not transcript_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Transcript not found"
        )

    return transcript_path.read_text(encoding="utf-8")

@app.put("/recordings/{recording_name}/transcript")
def update_transcript(
    recording_name: str,
    transcript: TranscriptUpdate
):

    transcript_path = TRANSCRIPT_DIR / f"{recording_name}.txt"

    if not transcript_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Transcript not found"
        )

    transcript_path.write_text(
        transcript.text,
        encoding="utf-8"
    )

    return {
        "message": "Transcript saved successfully",
        "recording": recording_name
    }

@app.get("/recordings/{recording_name}/audio")
def get_audio(recording_name: str):

    matching_files = list(UPLOAD_DIR.glob(f"{recording_name}.*"))

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="Audio recording not found"
        )

    return FileResponse(matching_files[0])