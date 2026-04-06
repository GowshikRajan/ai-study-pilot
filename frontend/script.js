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

function showSummaryResult(data) {
    output.innerHTML = "";
    const summaryCard = createElement("div", "summary-card");

    const title = createElement("h3", "summary-title", "Summary");
    summaryCard.appendChild(title);

    if (data.overview) {
        const overview = createElement("div", "summary-overview", data.overview);
        summaryCard.appendChild(overview);
    }

    if (Array.isArray(data.key_points) && data.key_points.length > 0) {
        const pointsLabel = createElement("div", "summary-subtitle", "Key points:");
        summaryCard.appendChild(pointsLabel);

        const list = createElement("ul", "summary-list");
        data.key_points.forEach((point) => {
            const item = createElement("li", undefined, point);
            list.appendChild(item);
        });
        summaryCard.appendChild(list);
    }

    if (!data.overview && !Array.isArray(data.key_points)) {
        const fallback = createElement("div", "text-result", JSON.stringify(data, null, 2));
        summaryCard.appendChild(fallback);
    }

    output.appendChild(summaryCard);
}

function showFlashcardsResult(data) {
    output.innerHTML = "";
    const flashcardContainer = createElement("div", "flashcard-container");

    const title = createElement("h3", "summary-title", "Flashcards");
    flashcardContainer.appendChild(title);

    if (!Array.isArray(data.flashcards) || data.flashcards.length === 0) {
        const fallback = createElement("div", "text-result", "No flashcards were generated.\n" + JSON.stringify(data, null, 2));
        flashcardContainer.appendChild(fallback);
        output.appendChild(flashcardContainer);
        return;
    }

    data.flashcards.forEach((flashcard, index) => {
        const card = createElement("div", "flashcard-card");
        const cardLabel = createElement("div", "flashcard-number", `Flashcard ${index + 1}`);
        const question = createElement("div", "flashcard-question", flashcard.question || "No question provided.");
        const answer = createElement("div", "flashcard-answer", flashcard.answer || "No answer provided.");

        card.appendChild(cardLabel);
        card.appendChild(question);
        card.appendChild(answer);
        flashcardContainer.appendChild(card);
    });

    output.appendChild(flashcardContainer);
}

function showJsonResult(data) {
    output.innerHTML = "";
    const pre = document.createElement("pre");
    pre.textContent = JSON.stringify(data, null, 2);
    output.appendChild(pre);
}

function showHistory() {
    showLoading("Loading past study materials...");

    fetch("/history", { credentials: "include" })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                showError(data.error);
                return;
            }

            if (!Array.isArray(data.history) || data.history.length === 0) {
                showTextResult("No past study materials were found for this session.");
                return;
            }

            renderHistory(data.history);
        })
        .catch((error) => {
            showError("Failed to load history. Please try again.");
            console.error(error);
        });
}

function renderHistory(items) {
    output.innerHTML = "";
    const historyContainer = createElement("div", "history-list");

    items.forEach((item) => {
        historyContainer.appendChild(renderHistoryItem(item));
    });

    output.appendChild(historyContainer);
}

function renderHistoryItem(item) {
    const card = createElement("div", "history-card");

    const header = createElement("div", "history-card-header");
    header.appendChild(createElement("div", "history-type", item.type || "Unknown"));
    header.appendChild(
        createElement(
            "div",
            "history-date",
            item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"
        )
    );
    card.appendChild(header);

    const data = item.data || {};

    if (item.type === "summary") {
        card.appendChild(createElement("div", "history-item-title", "Summary"));
        if (data.overview) {
            card.appendChild(createElement("div", "history-overview", data.overview));
        }
        if (Array.isArray(data.key_points) && data.key_points.length > 0) {
            const list = createElement("ul", "history-list-items");
            data.key_points.forEach((point) => {
                list.appendChild(createElement("li", undefined, point));
            });
            card.appendChild(list);
        }
    } else if (item.type === "flashcards") {
        card.appendChild(createElement("div", "history-item-title", "Flashcards"));
        if (Array.isArray(data.flashcards) && data.flashcards.length > 0) {
            data.flashcards.forEach((flashcard, idx) => {
                const flashNode = createElement("div", "history-flashcard");
                flashNode.appendChild(createElement("div", "flashcard-number", `#${idx + 1}`));
                flashNode.appendChild(createElement("div", "flashcard-question", flashcard.question || "No question provided."));
                flashNode.appendChild(createElement("div", "flashcard-answer", flashcard.answer || "No answer provided."));
                card.appendChild(flashNode);
            });
        }
    } else if (item.type === "quiz") {
        card.appendChild(createElement("div", "history-item-title", "Quiz"));
        if (Array.isArray(data.quiz) && data.quiz.length > 0) {
            data.quiz.forEach((quizItem, idx) => {
                const quizNode = createElement("div", "history-quiz-item");
                quizNode.appendChild(createElement("div", "history-quiz-question", `${idx + 1}. ${quizItem.question || "No question provided."}`));
                if (Array.isArray(quizItem.options)) {
                    const optionList = createElement("ul", "history-list-items");
                    quizItem.options.forEach((option) => {
                        optionList.appendChild(createElement("li", undefined, option));
                    });
                    quizNode.appendChild(optionList);
                }
                if (quizItem.answer_index !== undefined) {
                    const correct = quizItem.options && quizItem.options[quizItem.answer_index]
                        ? quizItem.options[quizItem.answer_index]
                        : "Unknown";
                    quizNode.appendChild(createElement("div", "history-quiz-answer", `Answer: ${correct}`));
                }
                card.appendChild(quizNode);
            });
        }
    } else {
        card.appendChild(createElement("pre", "history-raw", JSON.stringify(data, null, 2)));
    }

    return card;
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

    let response = await fetch("/generate-summary", {
        credentials: "include",
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

    if (typeof data === "string") {
        showTextResult(data);
        return;
    }

    if (data.overview || Array.isArray(data.key_points)) {
        showSummaryResult(data);
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

    let response = await fetch("/generate-flashcards", {
        credentials: "include",
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

    if (Array.isArray(data.flashcards)) {
        showFlashcardsResult(data);
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

    let response = await fetch("/generate-quiz", {
        credentials: "include",
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
