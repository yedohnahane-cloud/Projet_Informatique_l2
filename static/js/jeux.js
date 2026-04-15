/* =============================================
   JAVAMASTERAI – QUIZZS ET JEUX  |  games.js
   ============================================= */

const GAMES = [
  {
    id: 1,
    name: "CodinGame",
    url: "https://www.codingame.com/start/",
    emoji: "🦖",
    description: "Écrire du code Java pour attaquer, se défendre et vaincre un monstre.",
    img: "/static/images/jeux/image1.png"
  },
  {
    id: 2,
    name: "Robocode",
    url: "https://robocode.sourceforge.io/",
    emoji: "🤖",
    description: "Programmer un robot pour exécuter des actions et combattre.",
    img: "/static/images/jeux/image3.png"
  },
  {
    id: 3,
    name: "Codewars",
    url: "https://www.codewars.com/",
    emoji: "⚔️",
    description: "Résoudre des énigmes avec du code pour sortir d'une pièce.",
    img: "/static/images/jeux/image4.png"
  },
  {
    id: 4,
    name: "Screeps",
    url: "https://screeps.com/",
    emoji: "🚀",
    description: "Programmer les actions et trajectoires d'un vaisseau spatial.",
    img: "/static/images/jeux/image2.png"
  },
  {
    id: 5,
    name: "CheckiO",
    url: "https://checkio.org/",
    emoji: "🏙️",
    description: "Créer des bâtiments et structures via des classes Java.",
    img: "/static/images/jeux/image5.png"
  },
  {
    id: 6,
    name: "CodeCombat",
    url: "https://codecombat.com/",
    emoji: "🕵️",
    description: "Trouver et corriger des bugs pour résoudre des enquêtes.",
    img: "/static/images/jeux/image6.png"
  },
  {
    id: 7,
    name: "Javarush",
    url: "https://javarush.com/",
    emoji: "☕",
    description: "Apprendre Java à travers des mini-jeux et des quêtes interactives.",
    img:"/static/images/jeux/image7.png"
  },
  {
    id: 8,
    name: "HackerRank",
    url: "https://www.hackerrank.com/",
    emoji: "🏆",
    description: "Relever des défis de code Java pour grimper dans le classement mondial.",
    img: "/static/images/jeux/image8.jpg"
  },
  {
    id: 9,
    name: "LeetCode",
    url: "https://leetcode.com/",
    emoji: "🧩",
    description: "Résoudre des problèmes algorithmiques Java pour préparer tes entretiens.",
    img: "/static/images/jeux/image9.jpg"
  },
  {
    id: 10,
    name: "CodingBat",
    url: "https://codingbat.com/",
    emoji: "🦇",
    description: "Pratiquer Java avec des exercices courts et progressifs.",
    img: "/static/images/jeux/image10.jpg"
  }
];

/* ---- Build cards ---- */
function buildCards() {
  const grid = document.getElementById('games-grid');
  if (!grid) return;

  GAMES.forEach(game => {
    const card = document.createElement('a');
    card.href = game.url;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    card.className = 'game-card';
    card.setAttribute('aria-label', game.name);

    card.innerHTML = `
      <div class="card-thumb">
        <img
          src="${game.img}"
          alt="${game.name}"
          loading="lazy"
          onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
        />
        <div class="card-thumb-fallback" style="display:none;">${game.emoji}</div>
      </div>
      <div class="card-body">
        <p class="card-label">Description</p>
        <p class="card-title">${game.name}</p>
        <p class="card-desc">${game.description}</p>
      </div>
      <span class="card-play-badge">▶ Jouer</span>
    `;

    grid.appendChild(card);
  });
}

/* ---- Highlight active nav ---- */
function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  if (path.includes('coursprincipal')) {
    document.getElementById('nav-cours')?.classList.add('active');
  } else if (path.includes('chat-bot')) {
    document.getElementById('nav-chatbot')?.classList.add('active');
  } else {
    document.getElementById('nav-jeux')?.classList.add('active');
  }
}

/* ---- Init ---- */
document.addEventListener('DOMContentLoaded', () => {
  buildCards();
  setActiveNav();
});