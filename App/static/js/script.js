const record = document.getElementById("recordButton");
const output = document.getElementById("inputTextArea");
const socket = new WebSocket("ws://localhost:8000/ws/stt/");

let mediaRecorder;
let chunks = [];
let state = "stop";

if (navigator.mediaDevices.getUserMedia()) {
  function setupSuccess(stream) {
    console.log("setup success");
    mediaRecorder = new MediaRecorder(stream);

    record.addEventListener("click", (e) => {
      e.preventDefault();

      socket.onopen = () => {
        console.log("WebSocket connection established");
      };

      socket.onmessage = (event) => {
        // Display the transcription result
        const message = JSON.parse(event.data);
        if (message.text) {
          output.textContent += message.text + " ";
        }
      };

      if (mediaRecorder.state == "recording") {
        mediaRecorder.stop();
        chunks = [];
        record.style.backgroundColor = "rgb(7, 165, 120)";
        record.innerHTML = "Record";
      } else {
        mediaRecorder.start();
        record.style.backgroundColor = "rgb(255, 0, 93)";
        record.innerHTML = "Stop";
      }

      mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
        socket.send(e.data);
      };
    });
  }
  function setupFailure(e) {
    console.log("setup failure");
  }

  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then(setupSuccess)
    .catch(setupFailure);
} else {
  alert("Your browser does not support audio recording.");
}
