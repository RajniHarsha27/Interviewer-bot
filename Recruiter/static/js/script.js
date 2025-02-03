document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("questionForm");
  const button = document.getElementById("submit");

  form.addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent default form submission
    const jd = document.getElementById("jd").value.trim();
    const sampleQuestions = document
      .getElementById("sampleQuestions")
      .value.trim();
    const cvFile = document.getElementById("cv").files[0];
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();

    // Validate required fields
    if (!jd || !cvFile || !name || !email) {
      alert("Please fill in all required fields.");
      return;
    }

    button.innerText = "Assistant generating questions..";
    const formData = new FormData();
    formData.append("jd", jd);
    formData.append("sample_questions", sampleQuestions); // Optional
    formData.append("cv", cvFile);
    formData.append("name", name);
    formData.append("email", email);

    try {
      const response = await fetch("http://127.0.0.1:8003/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      button.innerText = "Generate Questions";
      const result = await response.json();

      alert(result.message);
    } catch (error) {
      console.error("Submission error:", error);
      alert("Failed to submit the form. Please try again.");
    }
  });
});
