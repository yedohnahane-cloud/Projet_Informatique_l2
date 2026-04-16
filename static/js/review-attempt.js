const scoreEl = document.getElementById("review-score");
const attemptNumberEl = document.getElementById("review-attempt-number");
const errorsContainer = document.getElementById("errors-container");

async function loadReviewAttempt() {
    try {
        const response = await fetch(reviewUrl);
        const data = await response.json();

        if (!response.ok) {
            scoreEl.textContent = data.error || "Impossible de charger la tentative.";
            attemptNumberEl.textContent = "";
            errorsContainer.innerHTML = "";
            return;
        }

        scoreEl.textContent = `Score : ${data.score}%`;
        attemptNumberEl.textContent = `Tentative n°${data.attempt_number}`;

        if (!data.errors || data.errors.length === 0) {
            errorsContainer.innerHTML = `
                <div class="error-card">
                    <h3>Aucune erreur</h3>
                    <p>Bravo, toutes les réponses sont correctes.</p>
                </div>
            `;
            return;
        }

        errorsContainer.innerHTML = data.errors.map((error, index) => `
            <div class="error-card">
                <h3>Erreur ${index + 1}</h3>
                <p><strong>Question :</strong> ${error.question_text}</p>
                <p><strong>Votre réponse :</strong> ${error.selected_choice ?? "Aucune réponse"}</p>
                <p><strong>Bonne réponse :</strong> ${error.correct_choice ?? "Non définie"}</p>
            </div>
        `).join("");

    } catch (error) {
        console.error(error);
        scoreEl.textContent = "Erreur réseau.";
        attemptNumberEl.textContent = "";
        errorsContainer.innerHTML = "";
    }
}

loadReviewAttempt();