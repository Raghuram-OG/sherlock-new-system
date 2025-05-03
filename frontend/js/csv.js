document.getElementById("download-csv").addEventListener("click", () => {
    const table = document.getElementById("data-table");
    const headers = Array.from(table.querySelectorAll("#table-header th")).map(th => th.textContent);
    const rows = Array.from(table.querySelectorAll("#table-body tr")).map(tr =>
        Array.from(tr.querySelectorAll("td")).map(td => td.textContent)
    );

    const csvContent = [
        headers.join(","),
        ...rows.map(row => row.join(","))
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${currentTable}.csv`;
    a.click();
    URL.revokeObjectURL(url);
});