const personnageImage = document.getElementById("personnageImage");
const personnageChoisi = localStorage.getItem("personnageChoisi");

if (personnageChoisi === "Lucie") {
    personnageImage.src = "/static/images/image_lucie.png";
    personnageImage.alt = "Lucie";
} else {
    personnageImage.src = "/static/images/image_leo.png";
    personnageImage.alt = "Leo";
}

const scoreText = document.getElementById("score-text");
const attemptText = document.getElementById("attempt-text");
const nextCourseBox = document.getElementById("next-course-box");
const reviewBtn = document.getElementById("review-errors-btn");

const storedResult = localStorage.getItem("quizResult");

if (storedResult) {
    const result = JSON.parse(storedResult);

    scoreText.textContent = `Score : ${result.score}%`;
    attemptText.textContent = `Tentative n°${result.attempt_number}`;

    const canReview = result.score >= 80 || result.attempt_count >= 3;

    if (reviewBtn && !canReview) {
        reviewBtn.style.opacity = "0.6";
        reviewBtn.style.pointerEvents = "none";
        reviewBtn.textContent = "Erreurs après 80% ou 3 essais";
    }

    if (result.next_course_unlocked && result.next_course_id) {
        nextCourseBox.innerHTML = `
            <p>Le chapitre suivant a été débloqué.</p>
            <a href="/courses/chapters/${result.next_course_id}/view/" class="action-btn">
                Aller au chapitre suivant
            </a>
        `;
    } else {
        nextCourseBox.innerHTML = `<p>Continuez vos révisions pour progresser.</p>`;
    }
} else {
    scoreText.textContent = "Aucun résultat trouvé.";
}
const resetBtn = document.getElementById("reset-attempts-btn");

// récupère le résultat du quiz
const storedResult = localStorage.getItem("quizResult");

if (storedResult) {
    const result = JSON.parse(storedResult);

    // afficher le bouton seulement si :
    // - 3 essais atteints
    // OU
    // - score >= 80
    const canReset = result.attempt_count >= 3 || result.score >= 80;

    if (resetBtn && canReset) {
        resetBtn.style.display = "inline-flex";
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

            // 🔥 TRÈS IMPORTANT
            localStorage.removeItem("quizResult");

            alert("Essais réinitialisés !");
            window.location.href = `/quiz/${quizId}/play/`;

        } catch (error) {
            console.error("Erreur reset:", error);
            alert("Erreur réseau.");
        }
    });
}

// fonction CSRF
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