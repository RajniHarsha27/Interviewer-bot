const recordButton = document.getElementById("record");
let statusBar = document.getElementById("statusBar");
const maxRecordingTime = 29000;
let seconds = 29;
let funcId = null;
let mediaStop = null;

let mediaRecorder;
let isRecording = false;

function formatTime(seconds) {
  const minute = Math.floor(seconds / 60);
  const second = seconds % 60;
  formatted_minute = minute.toString().padStart(2, "0");
  formatted_seconds = second.toString().padStart(2, "0");
  recordButton.innerHTML = `${formatted_minute}:${formatted_seconds}`;
}
function updateTime() {
  seconds--;
  formatTime(seconds);
}

function stopTimer() {
  clearInterval(funcId);
  seconds = 29;
  funcId = null;
}

function startTimer() {
  if (funcId == null) {
    funcId = setInterval(updateTime, 1000);
  }
}

// WebSocket setup:
const socket = new WebSocket("ws://localhost:8000/ws/audio"); // Replace with your WebSocket endpoint

// Open WebSocket connection and handle response from server
socket.onopen = () => {
  console.log("WebSocket connection established.");
};

socket.onmessage = (event) => {
  if (typeof event.data === "string") {
    const data = JSON.parse(event.data);
    if (data.transcript) {
      statusBar.innerHTML = "<br>";
      putResponse(data.transcript);
    } else if (data.answer) {
      console.log(data.answer);
      if (data.answer.trim() == "Thank you for your time. Goodbye!") {
        alert("Your answers are recorded. You can exit this webpage now.");
        recordButton.remove();
      }
      putAnswer(data.answer);
    }
  } else {
    let audioBlob = new Blob([event.data], { type: "audio/mpeg" });
    let audioUrl = URL.createObjectURL(audioBlob);
    let audioPlayer = document.createElement("audio");
    audioPlayer = document.createElement("audio");
    audioPlayer.id = "audio-player";
    historyArea.appendChild(audioPlayer);
    audioPlayer.src = audioUrl;

    audioPlayer.play();
    statusBar.textContent = "Bot speaking...";
    audioPlayer.addEventListener("ended", () => {
      statusBar.innerHTML = "<br>";
    });
  }
};

// Function to display response text
function putResponse(responseText) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chat-message");

  const messageContent = document.createElement("p");
  messageContent.textContent = responseText;

  messageDiv.appendChild(messageContent);

  const historyArea = document.getElementById("historyArea");
  historyArea.appendChild(messageDiv);
  historyArea.scrollTop = historyArea.scrollHeight;
}

function putAnswer(answerText) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chat-answer");

  const messageContent = document.createElement("p");
  messageContent.textContent = answerText;

  messageDiv.appendChild(messageContent);

  const historyArea = document.getElementById("historyArea");
  historyArea.appendChild(messageDiv);
  historyArea.scrollTop = historyArea.scrollHeight;
}

// Handle success of media stream
function setupSuccess(stream) {
  console.log("Setup Success");
  mediaRecorder = new MediaRecorder(stream);

  function handleStop() {
    const blob = new Blob(chunks, { type: "audio/mpeg" });
    chunks = [];
    statusBar.textContent = "Transcribing your answer...";

    // Send audio data via WebSocket
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(blob);
    }

    // Reset UI after stopping
    stopTimer();
    recordButton.innerText = "Record";
    recordButton.disabled = false; // Enable button again
  }

  function handleClick(e) {
    e.preventDefault();

    if (mediaRecorder.state === "inactive") {
      // Start recording
      chunks = [];
      mediaRecorder.start();
      startTimer();
      recordButton.innerText = "00:29";
      statusBar.textContent = "Recording your answer...";
      recordButton.disabled = true; // Disable button to prevent multiple clicks

      stopButton = document.createElement("button");
      stopButton.id = "stop";
      stopButton.classList.add("button");
      stopButton.innerHTML = "Stop";
      const buttonContainer = document.getElementById("buttons");
      buttonContainer.appendChild(stopButton); // Append to body or preferred container
      stopButton.addEventListener("click", handleStopRecordingManually);

      if (mediaStop) {
        clearTimeout(mediaStop);
        mediaStop = null;
      }

      // Auto-stop recording after 29 seconds
      mediaStop = setTimeout(() => {
        if (mediaRecorder.state === "recording") {
          mediaRecorder.stop();
          stopButton.remove();
        }
      }, maxRecordingTime);
    }
  }

  function handleStopRecordingManually(e) {
    e.preventDefault();
    if (mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      stopTimer();
      clearTimeout(mediaStop);
      mediaStop = null;
      recordButton.innerText = "Record";
      recordButton.disabled = false; // Enable record button again
      statusBar.textContent = "Recording stopped manually.";
      stopButton.remove(); // Remove stop button after stopping recording manually
    }
  }

  mediaRecorder.ondataavailable = (event) => chunks.push(event.data);
  mediaRecorder.onstop = handleStop;

  recordButton.addEventListener("click", handleClick);
}

// Handle failure to get the media stream
function setupFailure(error) {
  console.error("Failed to access user media:", error);
}

// Request access to the user's microphone
navigator.mediaDevices
  .getUserMedia({ audio: true })
  .then(setupSuccess)
  .catch(setupFailure);
