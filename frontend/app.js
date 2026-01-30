const API_URL = "http://127.0.0.1:8000/search";

async function searchPlaces() {
    const input = document.getElementById("searchInput").value;
    const container = document.getElementById("resultsContainer");
    const loading = document.getElementById("loading");

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
        const places = data.results || [];

        loading.classList.add("hidden");

        if (places.length === 0) {
            container.innerHTML = "<p>No places found matching that vibe. Try something else!</p>";
            return;
        }

        places.forEach(place => {
            let colorClass = 'price-red'; 
            let priceSign = '$$$';
            
            if (place.price === 'low') {
                colorClass = 'price-green';
                priceSign = '$';
            } else if (place.price === 'medium') {
                colorClass = 'price-yellow';
                priceSign = '$$';
            }

            const cardHTML = `
                <div>
                    <h3>${place.name}</h3>
                    <p>${place.description}</p>
                    
                    <div style="margin-top:10px;">
                        <span class="price-btn ${colorClass}">
                            ${priceSign} ${place.price ? place.price.toUpperCase() : 'STANDARD'}
                        </span>
                    </div>

                    ${place.promo ? '<p class="deal-text">✨ Student Deal Available!</p>' : ''}
                    
                    <p class="match-score">Match Score: ${(place.score * 100).toFixed(1)}%</p>
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

document.getElementById("searchInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        searchPlaces();
    }
});