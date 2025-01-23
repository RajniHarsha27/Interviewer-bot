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
  const data = JSON.parse(event.data);
  if (data.transcript) {
    putResponse(data.transcript); // Display the transcript from the server
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
