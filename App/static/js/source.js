const recordButton = document.getElementById("record");

let mediaRecorder;
let isRecording = false;
function putResponse(responseText) {
  // Create a new div to hold the chat message
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chat-message"); // Add 'chat-message' class for styling

  // Add the response text as a paragraph inside the new div
  const messageContent = document.createElement("p");
  messageContent.textContent = responseText;

  // Append the paragraph to the div
  messageDiv.appendChild(messageContent);

  // Get the historyArea by its ID and append the new message
  const historyArea = document.getElementById("historyArea");
  historyArea.appendChild(messageDiv);

  // Scroll to the bottom of the historyArea to show the new message
  historyArea.scrollTop = historyArea.scrollHeight;
}

// Handle success of media stream
function setupSuccess(stream) {
  console.log("Setup Success");
  mediaRecorder = new MediaRecorder(stream);

  function handleStop(event) {
    const blob = new Blob(chunks, { type: "audio/mpeg" });
    chunks = [];

    const formData = new FormData();
    formData.append("audio", blob);

    fetch("/transcribe", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        putResponse(data.transcript);
        console.log(data.transcript);
      });
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
