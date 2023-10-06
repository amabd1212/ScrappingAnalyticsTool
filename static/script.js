document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const location = document.getElementById("location").value;
    const language = document.getElementById("language").value;
    const number = document.getElementById("number").value;
    const search_for = document.getElementById("search-for").value;
    const search_term = document.getElementById("search-term").value;
    document.getElementById("enrich-button").style.display = "block"
    // Make an AJAX request to your Python backend
    fetch("/search", {
        method: "POST",
        body: JSON.stringify({
            location,
            language,
            number,
            search_for,
            search_term
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.country_not_available) {
            const messageContainer = document.getElementById("message-container");
            messageContainer.innerHTML = "Sorry, the country is not available or was typed incorrectly. A global search will be used.";
        }
        if (data.language_not_available) {
            const messageContainer = document.getElementById("message-container");
            messageContainer.innerHTML = "Sorry, the language is not available or was typed incorrectly. A search will be done in English.";
        }
        // Display the search results in the "results" div
        const resultsDiv = document.getElementById("results");
        resultsDiv.style.display = "none"; // Hide the div

        // Check if the CSV download link is available in the response
        if (data.csv_path) {
            const csvLink = document.getElementById('csv-link');
            csvLink.href = '/download_csv';  // Update the link to the download route
            csvLink.style.display = 'block'; // Show the CSV download link
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
// Add an event listener for the "Enrich" button
document.getElementById("enrich-button").addEventListener("click", function(event) {
    event.preventDefault();

    // Make an AJAX request to trigger the Selenium script
    fetch("/enrich", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);  // Print the result to the console

        // Show the link to download the enriched data
        const enrichedDataLink = document.getElementById('enriched-data-link');
        enrichedDataLink.href = result;  // Set the download link
        enrichedDataLink.style.display = 'block'; // Show the link
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

