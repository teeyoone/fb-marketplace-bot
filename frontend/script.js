document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("scrapeButton");
    if (button) {
      button.addEventListener("click", scrapeListings);
    } else {
      console.error("Scrape button not found.");
    }
  });
  
  async function scrapeListings() {
    const city = document.getElementById("city").value.trim();
    const query = document.getElementById("query").value.trim();
    const maxPrice = document.getElementById("maxPrice").value.trim();
    const responseDiv = document.getElementById("response");
  
    if (!city || !query || !maxPrice) {
      alert("Please fill in all fields.");
      return;
    }
  
    responseDiv.innerHTML = "<p>Loading listings...</p>";
  
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/crawl_facebook_marketplace?city=${encodeURIComponent(
          city
        )}&query=${encodeURIComponent(query)}&max_price=${encodeURIComponent(maxPrice)}`
      );
      const data = await res.json();
  
      console.log("Fetched Listings:", data);
  
      if (!Array.isArray(data) || data.length === 0) {
        responseDiv.innerHTML = "<p>No listings found.</p>";
        return;
      }
  
      // Clear previous listings
      responseDiv.innerHTML = "";
  
      // Render each unique listing
      const seen = new Set();
      data.forEach((item) => {
        const key = item.link; // or image if link is sometimes empty
        if (!item.title || !item.link || !item.image || seen.has(key)) return;
        seen.add(key);
  
        const itemDiv = document.createElement("div");
        itemDiv.style.marginBottom = "1.5em";
        itemDiv.style.borderBottom = "1px solid #ccc";
        itemDiv.style.paddingBottom = "1em";
  
        itemDiv.innerHTML = `
          <img src="${item.image}" alt="image" style="max-width: 100%; height: auto;"><br>
          <strong>${item.title}</strong><br>
          <span>${item.price}</span><br>
          <a href="${item.link}" target="_blank">View Listing</a><br>
          <small>${item.location}</small>
        `;
  
        responseDiv.appendChild(itemDiv);
      });
    } catch (err) {
      console.error("Fetch error:", err);
      responseDiv.innerHTML = "<p>Error fetching listings. Please check backend logs.</p>";
    }
  }
  