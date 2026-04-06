async function generateSummary() {
    let text = document.getElementById("inputText").value;

    if (!text) {
        alert("Please enter text first");
        return;
    }

    let response = await fetch("http://127.0.0.1:8001/generate-summary", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content: text })
    });

    let data = await response.json();
    document.getElementById("output").innerText = data.result || JSON.stringify(data);
}

async function generateFlashcards() {
    let text = document.getElementById("inputText").value;

    if (!text) {
        alert("Please enter text first");
        return;
    }

    let response = await fetch("http://127.0.0.1:8001/generate-flashcards", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content: text })
    });

    let data = await response.json();
    document.getElementById("output").innerText = JSON.stringify(data, null, 2);
}

async function generateQuiz() {
    let text = document.getElementById("inputText").value;

    if (!text) {
        alert("Please enter text first");
        return;
    }

    let response = await fetch("http://127.0.0.1:8001/generate-quiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content: text })
    });

    let data = await response.json();
    document.getElementById("output").innerText = JSON.stringify(data, null, 2);
}