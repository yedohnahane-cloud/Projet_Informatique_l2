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
const backCourseBtn = document.getElementById("back-course-btn");
const resetBtn = document.getElementById("reset-attempts-btn");

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

    if (canReview) {
        reviewBtn.style.display = "inline-flex";
        backCourseBtn.style.display = "none";
    } else {
        reviewBtn.style.display = "none";
        backCourseBtn.style.display = "inline-flex";
    }
    if (resetBtn && canReset) {
        resetBtn.style.display = "inline-flex";
    }

    if (nextCourseBox) {
        if (result.next_course_unlocked && result.next_course_id) {
            nextCourseBox.innerHTML = `
                <a href="/courses/chapters/${result.next_course_id}/view/" class="action-btn">
                    Aller au chapitre suivant
                </a>
            `;
        } else if (result.attempt_count >= 3 && result.next_course_id) {
            nextCourseBox.innerHTML = `
                <a href="/courses/chapters/${result.next_course_id}/view/" class="action-btn">
                    Passer au chapitre suivant
                </a>
            `;
        } else {
            nextCourseBox.innerHTML = `
    <div class="info-message warning">
        Continuez vos révisions pour progresser.
    </div>
`;
        }
    }
} else {
    if (scoreText) {
        scoreText.textContent = "Aucun résultat trouvé.";
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