const API_URL = "http://127.0.0.1:8000/search";

async function searchPlaces() {
    const input = document.getElementById("searchInput").value;
    const container = document.getElementById("resultsContainer");
    const loading = document.getElementById("loading");

    // Reset UI
    container.innerHTML = "";
    loading.classList.remove("hidden");

    if (!input) {
        alert("Please enter a vibe!");
        loading.classList.add("hidden");
        return;
    }

    try {
        const response = await fetch(`${API_URL}?query=${encodeURIComponent(input)}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Server Error");
        }

        const data = await response.json();
        
        // FIX 1: Access the 'results' list inside the object
        // The screenshot shows the list is inside data.results
        const places = data.results || [];

        loading.classList.add("hidden");

        if (places.length === 0) {
            container.innerHTML = "<p>No places found matching that vibe. Try something else!</p>";
            return;
        }

        // FIX 2: Use the property names exactly as shown in your screenshot
        // (name, description, price, promo) - No 'payload' needed!
        places.forEach(place => {
            // Handle price badge color
            let badgeColor = "medium"; // default yellow
            if (place.price === "low") badgeColor = "low";   // green
            if (place.price === "high") badgeColor = "high"; // red
            
            const cardHTML = `
                <div class="card">
                    <h3>${place.name}</h3>
                    <p>${place.description}</p>
                    <span class="badge ${badgeColor}">💰 ${place.price || 'Standard'}</span>
                    ${place.promo ? '<p class="promo">✨ Student Deal Available!</p>' : ''}
                    <small style="color: #bbb; display: block; margin-top: 10px;">Match Score: ${(place.score * 100).toFixed(1)}%</small>
                </div>
            `;
            container.innerHTML += cardHTML;
        });

    } catch (error) {
        console.error("Error:", error);
        loading.classList.add("hidden");
        container.innerHTML = `<p style="color: red; font-weight: bold;">❌ Error: ${error.message}</p>`;
    }
}

// Allow pressing "Enter" key to search
document.getElementById("searchInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        searchPlaces();
    }
});