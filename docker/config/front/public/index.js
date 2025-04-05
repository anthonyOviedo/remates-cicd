let allData = [];
let showingFavorites = false;

document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
    refreshData();
});

function setupEventListeners() {
    const filterInput = document.getElementById('province-filter');
    if (filterInput) {
        filterInput.addEventListener('input', renderItems);
    }

    const showFavBtn = document.getElementById('show-favorites');
    if (showFavBtn) {
        showFavBtn.addEventListener('click', () => {
            showingFavorites = true;
            renderItems();
        });
    }

    const showAllBtn = document.getElementById('show-all');
    if (showAllBtn) {
        showAllBtn.addEventListener('click', () => {
            showingFavorites = false;
            renderItems();
        });
    }
}

function refreshData() {
    fetch('/data')
        .then(res => res.json())
        .then(data => {
            const today = new Date().toISOString().split('T')[0];
            allData = data.filter(item => item.tercera_fecha >= today);
            renderItems();
        })
        .catch(error => console.error('Error fetching data:', error));
}

function renderItems() {
    const listContainer = document.getElementById('remates-list');
    const filterValue = (document.getElementById('province-filter')?.value || "").toLowerCase();

    const filtered = allData.filter(item =>
        item.ubicacion.toLowerCase().includes(filterValue) ||
        item.raw.toLowerCase().includes(filterValue)
    );

    const sorted = filtered.sort((a, b) => getClosestDate(a) - getClosestDate(b));
    const toRender = showingFavorites ? sorted.filter(item => item.favorito) : sorted;

    document.getElementById('filtered-count').textContent = `${toRender.length} Remates encontrados`;
    listContainer.innerHTML = toRender.length ? "" : "<p>No hay remates que mostrar.</p>";

    toRender.forEach((item, index) => listContainer.appendChild(createAuctionItem(item, index)));
}
function verMas(itemId) {
    if (itemId) {
        window.location.href = `/detalle?item=${encodeURIComponent(itemId)}`;
    }
}
function createAuctionItem(item, index) {
    const div = document.createElement('div');
    div.classList.add('auction-item'); // <--- ADD THIS

    div.innerHTML = `
        <p><span class="label">Ubicación:</span> ${item.ubicacion}</p>
        <p><span class="label">Medidas:</span> ${item.medidas} m²</p>
        <p><span class="label">Matricula:</span> ${item.matricula}</p>
        <p><span class="label">Juzgado:</span> ${item.juzgado}</p>
        <button class="favorite-btn" data-id="${item.id}">
            ${item.favorito ? '★' : '☆'}
        </button>
        <div class="dates">
            <p><strong>Primera fecha:</strong> ${item.primera_fecha} <span class="highlight">${item.precio.toLocaleString()} CRC</span></p>
        </div>

        <button  type="button"  class="btn btn-primary" onclick=verMas(${item.id}) data-id="${item.id}">
            Ver más
        </button>
    `;

    div.querySelector(".favorite-btn").addEventListener("click", () => toggleFavorite(item.id));
    return div;
}



function toggleFavorite(id) {
    const remate = allData.find(r => r.id === id);
    if (!remate) return;

    remate.favorito = !remate.favorito;

    fetch('/update-property', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: remate })
    })
        .then(res => res.json())
        .then(() => renderItems())
        .catch(err => console.error('Error updating favorito:', err));
}

function getClosestDate(item) {
    const today = new Date();
    const dates = [item.primera_fecha, item.segunda_fecha, item.tercera_fecha]
        .map(date => new Date(date))
        .filter(date => date >= today);
    return dates.length ? Math.min(...dates.map(d => d.getTime())) : Infinity;
}

// IA opinion feature
function aiopinion(prompt) {
    fetch('/ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    })
        .then(res => res.json())
        .then(data => showAIResponse(data.response))
        .catch(err => console.error('Error fetching AI response:', err));
}

function showAIResponse(text) {
    const modal = document.getElementById('aiModal');
    const textContainer = document.getElementById('aiResponseText');
    if (modal && textContainer) {
        textContainer.textContent = text;
        modal.style.display = "block";
    }
}

function closeModal() {
    const modal = document.getElementById('aiModal');
    if (modal) modal.style.display = "none";
}
