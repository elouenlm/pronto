try {
    if (typeof collegesData === 'undefined') {
        throw new Error("Le fichier 'mes_colleges.js' n'est pas chargé.");
    }

    // --- 1. NETTOYAGE ET ADAPTATION ---
    const vus = new Set();
    const cleanData = collegesData.map(c => {
        // On crée un petit décalage aléatoire pour que les points ne soient pas empilés
        const jitter = () => (Math.random() - 0.5) * 4;

        return {
            nom: c.nom || "Nom inconnu",
            ville: c.ville || "Ville inconnue",
            secteur: c.secteur || "?",
            ips: parseFloat(c.ips) || 0,
            taux: parseFloat(c.taux) || 0,
            lat: (c.lat === 46.0) ? 46.5 + jitter() : c.lat,
            lon: (c.lon === 2.0) ? 2.5 + jitter() : c.lon
        };
    }).filter(c => {
        const idUnique = c.nom + c.ville;
        if (c.ips <= 0 || vus.has(idUnique)) return false;
        vus.add(idUnique);
        return true;
    });

    // --- 2. RECHERCHE (Adaptée aux MAJUSCULES) ---
    const searchBar = document.getElementById('searchBar');
    searchBar.addEventListener('keyup', (e) => {
        const query = e.target.value.toLowerCase();
        const resultsDiv = document.getElementById('searchResults');
        resultsDiv.innerHTML = '';
        if (query.length < 2) return;

        const filtered = cleanData.filter(c =>
            c.nom.toLowerCase().includes(query) ||
            c.ville.toLowerCase().includes(query)
        ).slice(0, 10);

        filtered.forEach(c => {
            const diag = (ips) => {
                if (ips < 90) return { t: "Défavorisé", c: "diag-red" };
                if (ips < 110) return { t: "Moyen", c: "diag-gold" };
                return { t: "Favorisé", c: "diag-blue" };
            };
            const d = diag(c.ips);
            resultsDiv.innerHTML += `
                <div class="result-item">
                    <h3>🏫 ${c.nom}</h3>
                    <p>📍 ${c.ville} | IPS : <b>${c.ips}</b></p>
                    <p>🎓 Réussite : <b>${c.taux}%</b></p>
                    <p>Statut : <span class="${d.c}">${d.t}</span></p>
                </div>`;
        });
    });

    // --- 3. CARTE ---
    const map = L.map('map').setView([46.6, 2.4], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    cleanData.slice(0, 1500).forEach(c => {
        L.circleMarker([c.lat, c.lon], {
            radius: 5, color: c.taux > 90 ? '#3498db' : '#e74c3c', fillOpacity: 0.5
        }).addTo(map).bindPopup(`${c.nom}<br>Réussite: ${c.taux}%`);
    });

    // --- 4. GRAPHIQUE ---
    const ctx = document.getElementById('ipsChart').getContext('2d');
    const sections = ["<90", "90-110", ">110"];
    const stats = [
        cleanData.filter(c => c.ips < 90).reduce((a, b) => a + b.taux, 0) / cleanData.filter(c => c.ips < 90).length || 0,
        cleanData.filter(c => c.ips >= 90 && c.ips <= 110).reduce((a, b) => a + b.taux, 0) / cleanData.filter(c => c.ips >= 90 && c.ips <= 110).length || 0,
        cleanData.filter(c => c.ips > 110).reduce((a, b) => a + b.taux, 0) / cleanData.filter(c => c.ips > 110).length || 0
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sections,
            datasets: [{ label: 'Taux de réussite moyen (%)', data: stats, backgroundColor: ['#e74c3c', '#f1c40f', '#3498db'] }]
        },
        options: { maintainAspectRatio: false }
    });

} catch (e) { console.error(e); }