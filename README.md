# Teeth It To Me

A Greek medical/dental speech-to-text web application built to improve
transcription of dental terminology.

## What it does

- Converts Greek speech recordings into text using **faster-whisper**
- Uses a custom dental vocabulary to improve recognition of medical
  terms
- Applies custom corrections to common dental transcription errors
- Saves each recording and its transcript locally
- Provides a recording history so saved transcripts can be reopened and
  edited

## Tech Stack

- **Python**
- **FastAPI**
- **faster-whisper**
- **HTML / CSS / JavaScript**
- **REST API**
- **Git / GitHub**

## How it works

``` text
Audio Recording
      ↓
FastAPI
      ↓
faster-whisper
      ↓
Dental Term Correction
      ↓
Saved Transcript
```

Recordings are stored using a timestamp-based name, for example:

``` text
recording_20261008_142702.m4a
recording_20261008_142702.txt
```

The audio and transcript share the same name so they remain associated.

## Project Structure

``` text
TeethItToMe/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── main.py
│   └── medical_terms/
│       ├── dentistry.txt
│       └── dentistry_corrections.py
│
└── .gitignore
```

Local recordings, transcripts, and the Python virtual environment are
excluded from Git.

## Current Status

The core transcription and recording-history functionality is working.

### Next improvements

- Save manually edited transcripts
- Play saved recordings from the history
- Improve the recording history interface
- Further improve dental terminology accuracy
- Optimize GPU inference

## Why I built it

The project was created as a practical application of **Python, backend
development, APIs, speech-to-text, and testing** while solving a
specific problem: improving Greek speech transcription for dental
terminology.
