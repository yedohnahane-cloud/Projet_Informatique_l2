const personnageImage = document.getElementById("personnageImage");
const personnageChoisi = localStorage.getItem("personnageChoisi");

if (personnageImage) {
    if (personnageChoisi === "Lucie") {
        personnageImage.src = "/static/images/image_lucie.png";
        personnageImage.alt = "Lucie";
    } else {
        personnageImage.src = "/static/images/image_leo.png";
        personnageImage.alt = "Leo";
    }
}

const scoreText = document.getElementById("score-text");
const attemptText = document.getElementById("attempt-text");
const nextCourseBox = document.getElementById("next-course-box");
const reviewBtn = document.getElementById("review-errors-btn");
const resetBtn = document.getElementById("reset-attempts-btn");
const generateErrorsBtn = document.getElementById("generate-errors-btn");

const storedResult = localStorage.getItem("quizResult");

if (storedResult) {
    const result = JSON.parse(storedResult);

    if (scoreText) {
        scoreText.textContent = `Score : ${result.score}%`;
    }

    if (attemptText) {
        attemptText.textContent = `Tentative n°${result.attempt_number}`;
    }

    const canReview = result.score >= 80 || result.attempt_count >= 3;
    const canReset = result.attempt_count >= 3 || result.score >= 80;

    if (reviewBtn && !canReview) {
        reviewBtn.style.opacity = "0.6";
        reviewBtn.style.pointerEvents = "none";
        reviewBtn.textContent = "Erreurs après 80% ou 3 essais";
    }

    if (resetBtn && canReset) {
        resetBtn.style.display = "inline-flex";
    }

    if (generateErrorsBtn && !result.attempt_id) {
        generateErrorsBtn.disabled = true;
        generateErrorsBtn.style.opacity = "0.6";
        generateErrorsBtn.style.pointerEvents = "none";
    }

    if (nextCourseBox) {
        if (result.next_course_unlocked && result.next_course_id) {
            nextCourseBox.innerHTML = `
                <p>Le chapitre suivant a été débloqué.</p>
                <a href="/courses/chapters/${result.next_course_id}/view/" class="action-btn">
                    Aller au chapitre suivant
                </a>
            `;
        } else if (result.attempt_count >= 3 && result.next_course_id) {
            nextCourseBox.innerHTML = `
                <p>Vous avez atteint 3 essais. Vous pouvez réinitialiser vos essais ou passer au chapitre suivant.</p>
                <a href="/courses/chapters/${result.next_course_id}/view/" class="action-btn">
                    Passer au chapitre suivant
                </a>
            `;
        } else {
            nextCourseBox.innerHTML = `<p>Continuez vos révisions pour progresser.</p>`;
        }
    }
} else {
    if (scoreText) {
        scoreText.textContent = "Aucun résultat trouvé.";
    }

    if (generateErrorsBtn) {
        generateErrorsBtn.disabled = true;
        generateErrorsBtn.style.opacity = "0.6";
        generateErrorsBtn.style.pointerEvents = "none";
    }
}

if (resetBtn) {
    resetBtn.addEventListener("click", async () => {
        try {
            const response = await fetch(resetAttemptsUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Erreur lors de la réinitialisation.");
                return;
            }

            localStorage.removeItem("quizResult");
            alert("Essais réinitialisés !");
            window.location.href = `/quiz/${quizId}/play/`;

        } catch (error) {
            console.error("Erreur reset:", error);
            alert("Erreur réseau.");
        }
    });
}

if (generateErrorsBtn) {
    generateErrorsBtn.addEventListener("click", () => {
        const storedResult = localStorage.getItem("quizResult");

        if (!storedResult) {
            alert("Aucun résultat de quiz trouvé.");
            return;
        }

        const result = JSON.parse(storedResult);
        const attemptId = result.attempt_id;

        if (!attemptId) {
            alert("Impossible de générer le quiz d'erreurs : tentative introuvable.");
            return;
        }

        window.location.href = `/courses/chatbot/?attempt_id=${attemptId}`;
    });
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