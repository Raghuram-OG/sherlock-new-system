// const API_URL = "http://localhost:5000/api"; // Update with deployed URL (e.g., Vercel)
const API_URL = "sherlock-new-system.onrender.com/api"
let currentTable = "agents";
let daysFilter = 0; // Default to show all calls

document.getElementById("table-select").addEventListener("change", (e) => {
    currentTable = e.target.value;
    // Show filter container only for calls table 
    document.getElementById("filter-container").style.display = currentTable === "calls" ? "block" : "none";
    // Reset filter and error on table change
    document.getElementById("days-filter").value = "";
    document.getElementById("filter-error").style.display = "none";
    daysFilter = 0;
    loadTableData();
    loadChart();
});

document.getElementById("apply-filter")?.addEventListener("click", () => {
    const daysInput = document.getElementById("days-filter").value;
    const errorSpan = document.getElementById("filter-error");
    
    // Validate input
    if (daysInput === "" || isNaN(daysInput) || daysInput < 0) {
        errorSpan.textContent = "Please enter a valid number (0 or positive)";
        errorSpan.style.display = "inline";
        return;
    }
    
    errorSpan.style.display = "none";
    daysFilter = parseInt(daysInput); // Convert to integer
    console.log(`Applying filter: past ${daysFilter} days`);
    loadTableData();
});

async function loadTableData() {
    try {
        // Construct URL with days filter for calls table
        let url = `${API_URL}/${currentTable}`;
        if (currentTable === "calls" && daysFilter !== 0) {
            url += `?days=${daysFilter}`;
        }
        console.log(`Fetching data from: ${url}`);
        const response = await fetch(url);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to fetch ${currentTable} data: ${errorData.error || response.statusText}`);
        }
        const data = await response.json();
        console.log(`Received ${data.length} records for ${currentTable}`, data);
        if (!data || data.length === 0) {
            console.warn(`No data returned for ${currentTable}`);
            renderTable([]); // Ensure "No data available" is shown
            document.getElementById("filter-error").textContent = "No calls found for the selected filter";
            document.getElementById("filter-error").style.display = currentTable === "calls" ? "inline" : "none";
        } else {
            document.getElementById("filter-error").style.display = "none";
            renderTable(data);
        }
        document.getElementById("download-csv").style.display = data.length ? "block" : "none";
        updateChart(data);
    } catch (error) {
        console.error(`Error loading ${currentTable} data:`, error);
        renderTable([]);
        document.getElementById("filter-error").textContent = `Error: ${error.message}`;
        document.getElementById("filter-error").style.display = currentTable === "calls" ? "inline" : "none";
    }
}

// Initial load
document.getElementById("filter-container").style.display = currentTable === "calls" ? "block" : "none";
loadTableData();