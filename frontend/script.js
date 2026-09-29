let mediaRecorder;
let audioChunks = [];

let startTime;
let timerInterval;

// ELEMENTS

const recordButton = document.getElementById("recordButton");
const stopButton = document.getElementById("stopButton");

const statusText = document.getElementById("statusText");
const statusIndicator = document.getElementById("statusIndicator");

const timer = document.getElementById("timer");

const audioPlayer = document.getElementById("audioPlayer");

const transcription = document.getElementById("transcription");

const clearButton = document.getElementById("clearButton");

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

    statusText.textContent = "Η εγγραφή ολοκληρώθηκε.";

    statusIndicator.style.background = "#22c55e";

    stopTimer();

});

// TIMER

function startTimer() {

    startTime = Date.now();

    timerInterval = setInterval(() => {

        const elapsed =
            Math.floor((Date.now() - startTime) / 1000);

        const minutes =
            String(Math.floor(elapsed / 60)).padStart(2, "0");

        const seconds =
            String(elapsed % 60).padStart(2, "0");

        timer.textContent =
            `${minutes}:${seconds}`;

    }, 1000);

}

function stopTimer() {

    clearInterval(timerInterval);

}

// CLEAR TRANSCRIPTION

clearButton.addEventListener("click", () => {

    transcription.innerHTML =
        `<span class="placeholder">
            Η μεταγραφή θα εμφανιστεί εδώ...
        </span>`;

});

// TEMPORARY TRANSCRIPTION

function simulateTranscription() {

    transcription.innerHTML = `
        <p>
            <strong>Demo:</strong>
            Ο ασθενής παρουσιάζει συμπτώματα
            αρτηριακής υπέρτασης και αναφέρει
            περιστασιακή δύσπνοια.
        </p>
    `;

}