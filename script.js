// Persistent Dark Mode Across Pages
document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-mode");

    if (localStorage.getItem("dark-mode") === "enabled") {
        document.body.classList.add("dark-mode");
        toggleButton.textContent = "☀️";
    }

    toggleButton.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("dark-mode", "enabled");
            toggleButton.textContent = "☀️";
        } else {
            localStorage.setItem("dark-mode", "disabled");
            toggleButton.textContent = "🌙";
        }
    });
});


function predictDisease() {
    const symptoms = document.getElementById("symptoms").value.trim();
    if (!symptoms) {
        alert("Please enter symptoms before predicting.");
        return;
    }

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ symptoms: symptoms })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("disease-box").innerHTML = `🔍 <span class="highlight">${data.prediction}</span>`;
        document.getElementById("precautions-box").innerHTML = `💡 <span class="highlight">${data.precautions}</span>`;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("disease-box").innerHTML = "❌ Error fetching prediction.";
        document.getElementById("precautions-box").innerHTML = "⚠️ Please try again.";
    });
}
