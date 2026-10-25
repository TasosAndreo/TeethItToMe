let mediaRecorder;
let audioChunks = [];
let startTime;
let timerInterval;
let currentRecordingName = null;
let elapsedSeconds = 0;
let timerStartedAt = null;

// ELEMENTS

const recordButton = document.getElementById("recordButton");
const pauseButton = document.getElementById("pauseButton");
const stopButton = document.getElementById("stopButton");
const uploadButton = document.getElementById("uploadButton");
const audioFile = document.getElementById("audioFile");
const statusText = document.getElementById("statusText");
const statusIndicator = document.getElementById("statusIndicator");
const timer = document.getElementById("timer");
const audioPlayer = document.getElementById("audioPlayer");
const transcription = document.getElementById("transcriptionText");
const clearButton = document.getElementById("clearButton");
const recordingsList = document.getElementById("recordingsList");
const saveTranscriptButton = document.getElementById("saveTranscriptButton");
const saveStatus = document.getElementById("saveStatus");
const API_URL = "http://127.0.0.1:8000";

// LOAD RECORDINGS
async function loadRecordings() {

    try {

        const response = await fetch(
            `${API_URL}/recordings`
        );

        if (!response.ok) {
            throw new Error(
                `Server error: ${response.status}`
            );
        }

        const recordings = await response.json();

        displayRecordings(recordings);

    } catch (error) {

        console.error("Could not load recordings:", error);

        recordingsList.innerHTML = `
            <p>
                Δεν ήταν δυνατή η φόρτωση των εγγραφών.
            </p>
        `;
    }
}

// DISPLAY RECORDINGS
function displayRecordings(recordings) {

    if (recordings.length === 0) {

        recordingsList.innerHTML = `
            <p>
                Δεν υπάρχουν αποθηκευμένες εγγραφές.
            </p>
        `;

        return;
    }

    recordingsList.innerHTML = "";

    recordings.forEach(recording => {

        const recordingElement = document.createElement("div");

        recordingElement.className = "recording-item";

        recordingElement.innerHTML = `
            <span class="recording-name">
                ${recording.name}
            </span>

            <button
                class="open-recording-button"
                data-recording="${recording.name}"
            >
                Άνοιγμα
            </button>
        `;

        recordingsList.appendChild(recordingElement);
    });

}

// OPEN RECORDING
async function openRecording(recordingName) {

    try {

        const response = await fetch(
            `${API_URL}/recordings/${recordingName}/transcript`
        );

        if (!response.ok) {
            throw new Error(
                `Server error: ${response.status}`
            );
        }

        const text = await response.text();
        transcription.value = text;
        currentRecordingName = recordingName;

        statusText.textContent =
            `Άνοιξε: ${recordingName}`;

        statusIndicator.style.background = "#22c55e";

    } catch (error) {

        console.error("Could not load transcript:", error);

        statusText.textContent =
            "Δεν ήταν δυνατή η φόρτωση της μεταγραφής.";
    }
}

function updateTimerDisplay() {
    const minutes = String(
        Math.floor(elapsedSeconds / 60)
    ).padStart(2, "0");

    const seconds = String(
        elapsedSeconds % 60
    ).padStart(2, "0");

    timer.textContent = `${minutes}:${seconds}`;
}

function startTimer() {
    // Reset the timer for a new recording.
    elapsedSeconds = 0;
    timerStartedAt = Date.now();

    clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        elapsedSeconds = Math.floor(
            (Date.now() - timerStartedAt) / 1000
        );

        updateTimerDisplay();
    }, 250);

    updateTimerDisplay();
}

function pauseTimer() {
    if (timerStartedAt !== null) {
        elapsedSeconds = Math.floor(
            (Date.now() - timerStartedAt) / 1000
        );

        timerStartedAt = null;
    }

    clearInterval(timerInterval);
    timerInterval = null;

    updateTimerDisplay();
}

function resumeTimer() {
    if (timerStartedAt !== null) {
        return;
    }

    // Continue from the previously elapsed time.
    timerStartedAt = Date.now() - elapsedSeconds * 1000;

    clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        elapsedSeconds = Math.floor(
            (Date.now() - timerStartedAt) / 1000
        );

        updateTimerDisplay();
    }, 250);
}

function stopTimer() {
    if (timerStartedAt !== null) {
        elapsedSeconds = Math.floor(
            (Date.now() - timerStartedAt) / 1000
        );

        timerStartedAt = null;
    }

    clearInterval(timerInterval);
    timerInterval = null;

    updateTimerDisplay();
}

recordingsList.addEventListener("click", event => {

    const button = event.target.closest(
        ".open-recording-button"
    );

    if (!button) {
        return;
    }

    const recordingName =
        button.dataset.recording;

    openRecording(recordingName);
});

// START RECORDING
recordButton.addEventListener("click", async () => {

    try {

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        mediaRecorder = new MediaRecorder(stream);

        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {

            audioChunks.push(event.data);

        });

        mediaRecorder.addEventListener("stop", () => {

            const audioBlob = new Blob(audioChunks, {
                type: "audio/webm"
            });

            const audioUrl = URL.createObjectURL(audioBlob);

            audioPlayer.src = audioUrl;

            // Future backend integration
            simulateTranscription();

        });

        mediaRecorder.start();

        recordButton.disabled = true;
        stopButton.disabled = false;

        pauseButton.disabled = false;
        pauseButton.hidden = false;

        statusText.textContent = "Εγγραφή σε εξέλιξη...";

        statusIndicator.style.background = "#ef4444";

        startTimer();

    }

    catch (error) {

        console.error(error);

        statusText.textContent =
            "Δεν ήταν δυνατή η πρόσβαση στο μικρόφωνο.";

    }

});

// PAUSE / RESUME RECORDING
pauseButton.addEventListener("click", () => {
    if (!mediaRecorder) {
        return;
    }

    if (mediaRecorder.state === "recording") {
        mediaRecorder.pause();

        pauseButton.innerHTML = "▶ <span>Συνέχεια</span>";
        statusText.textContent = "Η εγγραφή έχει παύσει.";
        statusIndicator.style.background = "#f59e0b";

        pauseTimer();

    } else if (mediaRecorder.state === "paused") {
        mediaRecorder.resume();

        pauseButton.innerHTML = "⏸ <span>Παύση</span>";
        statusText.textContent = "Εγγραφή σε εξέλιξη...";
        statusIndicator.style.background = "#ef4444";

        resumeTimer();
    }
});

// STOP RECORDING
stopButton.addEventListener("click", () => {

    if (!mediaRecorder) {
        return;
    }

    mediaRecorder.stop();

    mediaRecorder.stream
        .getTracks()
        .forEach(track => track.stop());

    recordButton.disabled = false;
    stopButton.disabled = true;
    pauseButton.disabled = true;
    pauseButton.hidden = true;
    pauseButton.innerHTML = "⏸ <span>Παύση</span>";

    statusText.textContent = "Η εγγραφή ολοκληρώθηκε.";

    statusIndicator.style.background = "#22c55e";

    stopTimer();

});

// OPEN FILE SELECTOR
uploadButton.addEventListener("click", () => {

    audioFile.click();

});

// CLEAR TRANSCRIPTION
clearButton.addEventListener("click", () => {

    transcription.value = "";

});

audioFile.addEventListener("change", async () => {

    const file = audioFile.files[0];

    if (!file) {
        return;
    }

    // Show the selected audio in the player
    const audioUrl = URL.createObjectURL(file);
    audioPlayer.src = audioUrl;

    // Update status
    statusText.textContent =
        `Αρχείο: ${file.name}`;

    statusIndicator.style.background = "#2563eb";

    // Show transcription status
    transcription.value = "Transcribing...";

    try {

        const formData = new FormData();

        formData.append("file", file);

        const response = await fetch(
            `${API_URL}/transcribe`,
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error(
                `Server error: ${response.status}`
            );
        }

        const correctedText = await response.text();

        // Convert literal "\n" sequences into actual line breaks.
        const formattedText = correctedText.replace(/\\n/g, "\n");

        transcription.value = formattedText;

        // Refresh saved recordings
        await loadRecordings();

        statusText.textContent =
            "Η μεταγραφή ολοκληρώθηκε.";

        statusIndicator.style.background = "#22c55e";

    } catch (error) {

        console.error(error);

        transcription.value =
        `Error during transcription: ${error.message}`;

        statusText.textContent =
            "Σφάλμα κατά τη μεταγραφή.";

        statusIndicator.style.background = "#ef4444";
    }
});

saveTranscriptButton.addEventListener("click", async () => {
    // Make sure a saved recording is currently open.
    if (!currentRecordingName) {
        saveStatus.textContent = "Please open a saved transcript first.";
        return;
    }

    saveTranscriptButton.disabled = true;
    saveStatus.textContent = "Saving transcript...";

    try {
        const response = await fetch(
            `${API_URL}/recordings/${currentRecordingName}/transcript`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: transcription.value
                })
            }
        );

        if (!response.ok) {
            const errorDetails = await response.text();
            throw new Error(
                `Server error ${response.status}: ${errorDetails}`
            );
        }

        saveStatus.textContent = "Transcript saved successfully.";
        statusText.textContent = `Saved: ${currentRecordingName}`;
        statusIndicator.style.background = "#22c55e";

    } catch (error) {
        console.error("Could not save transcript:", error);
        saveStatus.textContent = `Save failed: ${error.message}`;
        statusIndicator.style.background = "#ef4444";

    } finally {
        saveTranscriptButton.disabled = false;
    }
});

loadRecordings();