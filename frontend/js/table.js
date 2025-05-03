function renderTable(data) {
    const header = document.getElementById("table-header");
    const body = document.getElementById("table-body");

    if (!data || data.length === 0) {
        header.innerHTML = "";
        body.innerHTML = "<tr><td colspan='100'>No data available</td></tr>";
        return;
    }

    // Define columns, excluding 'onboarding' and handling missing full_name
    const headers = Object.keys(data[0]).filter(h => h !== "onboarding");
    const headerRow = headers
        .map(h => `<th>${h === "full_name" ? "Agent Name" : h.replace(/_/g, " ").toUpperCase()}</th>`)
        .join("");
    const bodyRows = data
        .map(row => {
            return `<tr>${headers.map(h => `<td>${row[h] !== null && row[h] !== undefined ? row[h] : ""}</td>`).join("")}</tr>`;
        })
        .join("");

    header.innerHTML = `<tr>${headerRow}</tr>`;
    body.innerHTML = bodyRows;
}