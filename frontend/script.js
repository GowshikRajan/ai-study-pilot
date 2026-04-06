const output = document.getElementById("output");

const quizState = {
    quiz: [],
    currentQuestionIndex: 0,
    selectedOptionIndex: null,
    answered: false,
    score: 0,
};

function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
}

function showLoading(message = "Generating quiz...") {
    output.innerHTML = "";
    const loading = createElement("div", "loading", message);
    output.appendChild(loading);
}

function showError(message) {
    output.innerHTML = "";
    const error = createElement("div", "error-message", message);
    output.appendChild(error);
}

function showTextResult(message) {
    output.innerHTML = "";
    const textBlock = createElement("div", "text-result", message);
    output.appendChild(textBlock);
}

function showJsonResult(data) {
    output.innerHTML = "";
    const pre = document.createElement("pre");
    pre.textContent = JSON.stringify(data, null, 2);
    output.appendChild(pre);
}

function resetQuizState() {
    quizState.currentQuestionIndex = 0;
    quizState.selectedOptionIndex = null;
    quizState.answered = false;
    quizState.score = 0;
}

function renderQuiz() {
    output.innerHTML = "";

    const quiz = quizState.quiz;
    if (!Array.isArray(quiz) || quiz.length === 0) {
        showError("Quiz data is not available or contains no questions.");
        return;
    }

    const questionData = quiz[quizState.currentQuestionIndex];
    const questionCard = createElement("div", "quiz-card");

    const header = createElement("div", "quiz-header");
    header.appendChild(
        createElement(
            "div",
            "quiz-number",
            `Question ${quizState.currentQuestionIndex + 1} of ${quiz.length}`
        )
    );

    const instructions = createElement(
        "div",
        "quiz-tip",
        quizState.answered
            ? "Review your answer, then continue to the next question."
            : "Select an answer and submit to check yourself."
    );
    header.appendChild(instructions);
    questionCard.appendChild(header);

    const questionText = createElement("div", "quiz-question", questionData.question || "No question text available.");
    questionCard.appendChild(questionText);

    const optionsWrapper = createElement("div", "quiz-options");

    if (!Array.isArray(questionData.options) || questionData.options.length === 0) {
        const missing = createElement("div", "quiz-feedback", "No answer options were provided for this question.");
        questionCard.appendChild(missing);
        output.appendChild(questionCard);
        return;
    }

    questionData.options.forEach((optionText, index) => {
        const optionButton = createElement("button", "quiz-option", optionText || "Untitled answer");
        optionButton.type = "button";
        optionButton.disabled = quizState.answered;

        if (quizState.answered) {
            const correctIndex = Number(questionData.answer_index);
            if (index === correctIndex) {
                optionButton.classList.add("correct");
            }
            if (quizState.selectedOptionIndex === index && index !== correctIndex) {
                optionButton.classList.add("incorrect");
            }
        } else {
            if (quizState.selectedOptionIndex === index) {
                optionButton.classList.add("selected");
            }
            optionButton.addEventListener("click", () => {
                quizState.selectedOptionIndex = index;
                renderQuiz();
            });
        }

        optionsWrapper.appendChild(optionButton);
    });

    questionCard.appendChild(optionsWrapper);

    const controls = createElement("div", "quiz-controls");
    const actionButton = createElement(
        "button",
        "quiz-action-button",
        quizState.answered
            ? quizState.currentQuestionIndex < quiz.length - 1
                ? "Next Question"
                : "See Results"
            : "Submit Answer"
    );
    actionButton.type = "button";
    actionButton.disabled = !quizState.answered && quizState.selectedOptionIndex === null;
    actionButton.addEventListener("click", () => {
        if (quizState.answered) {
            goToNextQuestion();
        } else {
            submitQuizAnswer();
        }
    });

    controls.appendChild(actionButton);

    const resetButton = createElement("button", "quiz-action-button", "Restart Quiz");
    resetButton.type = "button";
    resetButton.addEventListener("click", () => {
        resetQuizState();
        renderQuiz();
    });
    controls.appendChild(resetButton);

    questionCard.appendChild(controls);

    if (quizState.answered) {
        const correctIndex = Number(questionData.answer_index);
        const isCorrect = quizState.selectedOptionIndex === correctIndex;
        const feedbackText = isCorrect
            ? "Nice work — your answer is correct."
            : `Incorrect. The right answer is: ${questionData.options[correctIndex] || "(unknown)"}.`;

        const feedback = createElement("div", "quiz-feedback", feedbackText);
        questionCard.appendChild(feedback);

        if (questionData.explanation) {
            const explanationBlock = createElement("div", "quiz-feedback", questionData.explanation);
            questionCard.appendChild(explanationBlock);
        }
    }

    output.appendChild(questionCard);
}

function submitQuizAnswer() {
    const questionData = quizState.quiz[quizState.currentQuestionIndex];
    if (quizState.selectedOptionIndex === null || !questionData) {
        return;
    }

    const correctIndex = Number(questionData.answer_index);
    const isCorrect = quizState.selectedOptionIndex === correctIndex;
    if (isCorrect) quizState.score += 1;
    quizState.answered = true;
    renderQuiz();
}

function goToNextQuestion() {
    if (quizState.currentQuestionIndex < quizState.quiz.length - 1) {
        quizState.currentQuestionIndex += 1;
        quizState.selectedOptionIndex = null;
        quizState.answered = false;
        renderQuiz();
        return;
    }

    showQuizSummary();
}

function showQuizSummary() {
    output.innerHTML = "";
    const summaryCard = createElement("div", "quiz-summary-card");

    const title = createElement("div", "quiz-result-title", "Quiz Complete");
    summaryCard.appendChild(title);

    const scoreText = createElement(
        "div",
        "quiz-result-score",
        `You answered ${quizState.score} of ${quizState.quiz.length} questions correctly.`
    );
    summaryCard.appendChild(scoreText);

    const reviewText = createElement("div", "quiz-summary", "Review each question or restart the quiz to try again.");
    summaryCard.appendChild(reviewText);

    const controls = createElement("div", "quiz-controls");
    const restartButton = createElement("button", "quiz-action-button", "Restart Quiz");
    restartButton.type = "button";
    restartButton.addEventListener("click", () => {
        resetQuizState();
        renderQuiz();
    });
    controls.appendChild(restartButton);

    const reviewButton = createElement("button", "quiz-action-button", "Review Questions");
    reviewButton.type = "button";
    reviewButton.addEventListener("click", () => {
        quizState.currentQuestionIndex = 0;
        quizState.selectedOptionIndex = null;
        quizState.answered = false;
        renderQuiz();
    });
    controls.appendChild(reviewButton);

    summaryCard.appendChild(controls);
    output.appendChild(summaryCard);
}

async function generateSummary() {
    let text = document.getElementById("inputText").value;

    if (!text) {
        alert("Please enter text first");
        return;
    }

    showLoading("Generating summary...");

    let response = await fetch("http://127.0.0.1:8001/generate-summary", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: text }),
    });

    let data = await response.json();
    if (data.error) {
        showError(data.error);
        return;
    }

    if (typeof data === "string" || data.result) {
        showTextResult(data.result || data);
        return;
    }

    showJsonResult(data);
}

async function generateFlashcards() {
    let text = document.getElementById("inputText").value;

    if (!text) {
        alert("Please enter text first");
        return;
    }

    showLoading("Generating flashcards...");

    let response = await fetch("http://127.0.0.1:8001/generate-flashcards", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: text }),
    });

    let data = await response.json();
    if (data.error) {
        showError(data.error);
        return;
    }

    showJsonResult(data);
}

async function generateQuiz() {
    let text = document.getElementById("inputText").value;

    if (!text) {
        alert("Please enter text first");
        return;
    }

    quizState.quiz = [];
    resetQuizState();
    showLoading("Creating an interactive quiz...");

    let response = await fetch("http://127.0.0.1:8001/generate-quiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: text }),
    });

    let data = await response.json();
    if (data.error) {
        showError(data.error);
        return;
    }

    if (!data || !Array.isArray(data.quiz) || data.quiz.length === 0) {
        showError("The quiz service returned an unexpected format. Please try again.");
        return;
    }

    quizState.quiz = data.quiz;
    renderQuiz();
}
