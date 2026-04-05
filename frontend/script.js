function generateSummary() {
    let text = document.getElementById("inputText").value;
    if (!text) {
        alert("Please enter text first");
        return;
    }
    alert("Summary clicked with text: " + text);
}

function generateFlashcards() {
    let text = document.getElementById("inputText").value;
    if (!text) {
        alert("Please enter text first");
        return;
    }
    alert("Flashcards clicked with text: " + text);
}

function generateQuiz() {
    let text = document.getElementById("inputText").value;
    if (!text) {
        alert("Please enter text first");
        return;
    }
    alert("Quiz clicked with text: " + text);
}
