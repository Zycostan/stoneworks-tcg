// Function to generate random stats
function generateRandomStats() {
    return {
        attack: Math.floor(Math.random() * 100) + 1,
        defense: Math.floor(Math.random() * 100) + 1,
    };
}

// Function to create a card
function createCard(image) {
    const stats = generateRandomStats();

    const card = document.createElement('div');
    card.className = 'card';

    const img = document.createElement('img');
    img.src = `skins/${image}`;
    img.alt = 'Player Image';

    const statsDiv = document.createElement('div');
    statsDiv.className = 'stats';
    statsDiv.innerHTML = `
        <p><strong>Attack:</strong> ${stats.attack}</p>
        <p><strong>Defense:</strong> ${stats.defense}</p>
    `;

    card.appendChild(img);
    card.appendChild(statsDiv);

    return card;
}

// Function to fetch and render cards
async function renderCards() {
    const container = document.getElementById('card-container');
    try {
        const response = await fetch('/api/images');
        const images = await response.json();
        images.forEach(image => {
            const card = createCard(image);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to load images:', error);
    }
}

// Render the cards on page load
renderCards();
