# Teeth It To Me

Greek speech-to-text for dental and CBCT (cone-beam computed tomography) diagnostic reports.

Teeth It To Me is a local web application that transcribes Greek audio using Faster-Whisper, applies custom dental terminology corrections, and lets users review and edit saved transcripts.

## Features

- Transcription of Greek audio recordings.
- Dental and CBCT terminology prompts to guide speech recognition.
- Custom corrections for selected dental terms.
- Local storage of audio recordings and transcripts.
- History of saved recordings.
- Editable transcripts with the ability to save changes.
- Spoken “next bullet” commands formatted as bullet points.

**Important:** Machine-generated transcripts may contain errors, especially with specialized medical terminology. Always review and verify the transcript before using it in a clinical report.

## Project Structure

```text
TeethItToMe/
├── backend/
│   ├── main.py
│   ├── medical_terms/
│   │   ├── dentistry.txt
│   │   └── dentistry_corrections.py
│   ├── recordings/
│   │   ├── audio/
│   │   └── transcripts/
│   └── venv/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt
├── README.md
└── .gitignore
```

The `venv/` directory contains a local Python virtual environment and should not be committed to GitHub.

## Requirements

- Python 3
- pip
- Internet access for the initial Whisper model download, if required
- Sufficient memory and disk space for the selected model

GPU acceleration may require additional platform-specific configuration. Start with the device configuration supported by your computer.

## Installation

Run these commands from the repository root.

### 1. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv backend\venv
.\backend\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

With the virtual environment activated:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure the model

Check `backend/main.py` for the Faster-Whisper model name and device configuration. The model may download automatically the first time it is used.

GPU support is not guaranteed to work automatically on every operating system or hardware configuration.

## Running the Application

### 1. Start the backend

From the repository root:

```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Keep the terminal open while using the application. Press `Ctrl+C` to stop the server.

FastAPI documentation:

http://127.0.0.1:8000/docs

### 2. Open the frontend

Open `frontend/index.html` in your browser.

The frontend currently connects to:

```text
http://127.0.0.1:8000
```

If you change the backend address or port, update `API_URL` in `frontend/script.js`.

If browser security or CORS issues occur when opening the HTML file directly, use a local frontend development server and configure the backend to allow its origin.

## Using the Application

1. Start the backend server.
2. Open the frontend.
3. Select an audio recording.
4. Wait for transcription to finish.
5. Review and correct the generated text.
6. Open a saved recording from the history to view its transcript.
7. Edit the transcript and save your changes.

Audio files and transcripts are stored locally in `backend/recordings/audio/` and `backend/recordings/transcripts/`.

## Dental Terminology

The `backend/medical_terms/` directory contains resources used by the transcription pipeline:

- `dentistry.txt` — dental and anatomical terminology used to guide recognition.
- `dentistry_corrections.py` — custom post-processing corrections for selected recognition errors.

Changes to these resources should be tested against representative recordings and verified reference transcripts. Terminology prompts can influence recognition but cannot guarantee correct spelling or clinical interpretation.

## Privacy and Clinical Use

- Treat recordings and transcripts as potentially sensitive medical information.
- Never commit patient audio, transcripts, or identifiable clinical data to a public repository.
- Follow applicable data-protection and professional requirements when processing real patient information.
- This application assists transcription; it does not replace clinical review, diagnosis, or approval of a final report.

## Contributing

Bug reports, suggestions, and contributions are welcome. Changes to transcription behavior should be tested using representative Greek dental recordings and verified reference transcripts.