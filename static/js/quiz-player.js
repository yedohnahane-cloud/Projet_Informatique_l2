let quizData = null;
let currentQuestionIndex = 0;
let answers = {};

const progressEl = document.getElementById("progress");
const questionNumberEl = document.getElementById("question-number");
const questionTextEl = document.getElementById("question-text");
const answersContainer = document.getElementById("answers-container");
const nextBtn = document.getElementById("next-btn");

async function loadQuiz() {
    try {
        const response = await fetch(quizStartUrl);
        const data = await response.json();

        if (!response.ok) {
            if (data.error && data.error.includes("Nombre maximal de tentatives atteint")) {
                window.location.href = quizResultUrl;
                return;
            }

            questionTextEl.textContent = data.error || "Erreur lors du chargement du quiz.";
            nextBtn.disabled = true;
            return;
        }

        quizData = data;
        renderQuestion();
    } catch (error) {
        questionTextEl.textContent = "Erreur réseau.";
        nextBtn.disabled = true;
        console.error(error);
    }
}

function renderQuestion() {
    const question = quizData.questions[currentQuestionIndex];
    const total = quizData.questions.length;

    progressEl.textContent = `${currentQuestionIndex + 1}/${total}`;
    questionNumberEl.textContent = String(currentQuestionIndex + 1).padStart(2, "0");
    questionTextEl.textContent = question.text;

    answersContainer.innerHTML = question.choices.map(choice => `
        <label class="answer">
            <input 
                type="radio" 
                name="question_${question.id}" 
                value="${choice.id}"
                ${answers[question.id] == choice.id ? "checked" : ""}
            >
            <div class="answer-content">
                <span>${choice.text}</span>
                <div class="circle"></div>
            </div>
        </label>
    `).join("");

    if (currentQuestionIndex === total - 1) {
        nextBtn.textContent = "Terminer";
    } else {
        nextBtn.textContent = "Suivant";
    }
}

nextBtn.addEventListener("click", async () => {
    const question = quizData.questions[currentQuestionIndex];
    const selected = document.querySelector(`input[name="question_${question.id}"]:checked`);

    if (!selected) {
        alert("Veuillez sélectionner une réponse.");
        return;
    }

    answers[question.id] = selected.value;

    if (currentQuestionIndex < quizData.questions.length - 1) {
        currentQuestionIndex++;
        renderQuestion();
    } else {
        await submitQuiz();
    }
});

async function submitQuiz() {
    try {
        const response = await fetch(`/quiz/${quizId}/submit/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ answers: answers })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Erreur lors de la soumission du quiz.");
            return;
        }

        localStorage.setItem("quizResult", JSON.stringify(data));
        window.location.href = `/quiz/${quizId}/result/`;
    } catch (error) {
        console.error(error);
        alert("Erreur réseau lors de la soumission.");
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

loadQuiz();