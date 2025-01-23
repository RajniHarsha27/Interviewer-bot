const recordButton = document.getElementById("record");

let mediaRecorder;
let isRecording = false;

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
      putResponse(data.transcript);
    } else if (data.answer) {
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

  function handleStop(event) {
    const blob = new Blob(chunks, { type: "audio/mpeg" });
    chunks = [];

    // Send audio data via WebSocket
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(blob); // Send audio file as binary data over WebSocket
    }
  }

  let chunks = [];
  function handleClick(e) {
    e.preventDefault();
    if (mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      recordButton.innerText = "Record";
    } else {
      mediaRecorder.start();
      recordButton.innerText = "Stop";
    }

    mediaRecorder.ondataavailable = (event) => {
      chunks.push(event.data);
    };

    mediaRecorder.onstop = (event) => handleStop(event);
  }

  recordButton.addEventListener("click", (e) => handleClick(e));
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
