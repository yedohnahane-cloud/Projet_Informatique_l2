
const personnages = [
  {
    nom: "Lucie",
    image: "image_lucie.png",
    stats: ["Rigoureuse", "Méthodique", "Analytique"]
  },
  {
    nom: "Leo",
    image: "image_leo.png",
    stats: ["Dynamique", "Motivant", "Stimulant"]
  }
];

let index = 0;

// éléments
const nomPerso = document.querySelector(".nom-perso");
const imagePerso = document.querySelector(".perso img");
const stats = document.querySelectorAll(".stat-nom");

// ===== BOUTON DROITE =====
document.querySelector(".droite-fleche").addEventListener("click", () => {
  index = (index + 1) % personnages.length;
  updatePerso();
});

// ===== BOUTON GAUCHE =====
document.querySelector(".gauche-fleche").addEventListener("click", () => {
  index = (index - 1 + personnages.length) % personnages.length;
  updatePerso();
});

// ===== UPDATE =====
function updatePerso(){
  nomPerso.textContent = personnages[index].nom;
  imagePerso.src = personnages[index].image;

  stats.forEach((stat, i) => {
    stat.textContent = personnages[index].stats[i];
  });
}


const choisirBtn = document.getElementById("choisirBtn");

choisirBtn.addEventListener("click", () => {

  if(personnages[index].nom === "Lucie"){
    window.location.href = "lucie_choisi.html";
  }
  else if(personnages[index].nom === "Leo"){
    window.location.href = "leo_choisi.html";
  }

});