const personnages = [
  {
    nom: "Lucie",
    image: "/static/images/image_lucie.png",
    stats: ["Rigoureuse", "Méthodique", "Analytique"]
  },
  {
    nom: "Leo",
    image: "/static/images/image_leo.png",
    stats: ["Dynamique", "Motivant", "Stimulant"]
  }
];

let index = 0;

const nomPerso = document.querySelector(".nom-perso");
const imagePerso = document.querySelector(".perso img");
const stats = document.querySelectorAll(".stat-nom");
const choisirBtn = document.getElementById("choisirBtn");
const titrePerso = document.getElementById("titrePerso");
const texteChoix = document.getElementById("texteChoix");
const selectedCharacterInput = document.getElementById("selectedCharacterInput");

document.querySelector(".droite-fleche").addEventListener("click", () => {
  index = (index + 1) % personnages.length;
  updatePerso();
});

document.querySelector(".gauche-fleche").addEventListener("click", () => {
  index = (index - 1 + personnages.length) % personnages.length;
  updatePerso();
});

function updatePerso() {
  nomPerso.textContent = personnages[index].nom;
  imagePerso.src = personnages[index].image;

  stats.forEach((stat, i) => {
    stat.textContent = personnages[index].stats[i];
  });

  if (selectedCharacterInput) {
    selectedCharacterInput.value = personnages[index].nom;
  }
}

choisirBtn.addEventListener("click", () => {
  const personnageActuel = personnages[index].nom;

  titrePerso.innerHTML = `Vous avez choisi <span>${personnageActuel}</span>`;
  texteChoix.style.display = "block";
  texteChoix.innerHTML = `Clique sur <strong>Créer un compte</strong> et code avec <span>${personnageActuel}</span>`;
  choisirBtn.style.display = "none";

  localStorage.setItem("personnageChoisi", personnageActuel);

  if (selectedCharacterInput) {
    selectedCharacterInput.value = personnageActuel;
  }
});

updatePerso();