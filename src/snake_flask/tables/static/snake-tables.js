// +------------------------------------------------------------------- INFO -+
// | [Snake-Flask/src/snake_flask/tables/static/snake-tables.js]               |
// |                                                                           |
// | Author      : Pascal Malouin (https://github.com/fantomH)                 |
// | Created     : 2026-05-25 18:09:11 UTC                                     |
// | Updated     : 2026-06-24 16:08:19 UTC                                     |
// | Description : SnakeTables js.                                             |
// +---------------------------------------------------------------------------+

/*
[+] Snake Table

Frontend engine for the Flask TableGenerator plugin.

Features:
- AJAX table loading
- Pagination
- Global search
- Column sorting
- Column resizing
- Drag & drop column reordering
- Click-to-copy cells

The backend endpoint is expected to return JSON:

{
    rows: [...],
    page: 1,
    page_size: 25,
    total: 500
}
*/

document.addEventListener("DOMContentLoaded", () => {
    // Initialize all snake tables once the page is loaded.

    // Find every table container with class "snake-table"
    // and initialize it.
    document.querySelectorAll(".snake-table").forEach(initSnakeTable);
});

function getColumns(container) {
    // Extract column definitions from the table headers.
    /*
    Reads:
        data-column
        data-type
    
    from each <th> element.
    
    Returns:
    [
        {
            name: "username",
            type: "text"
        },
        ...
    ]
    */
    return [...container.querySelectorAll("thead th")]
        .map(th => ({
            name: th.dataset.column,
            type: th.dataset.type || "text",
            url: th.dataset.url || "",
            text: th.dataset.text || "",
            class: th.dataset.class || "",
        }));
}

function initSnakeTable(container) {
    // Initialize a single snake table instance.

    // Internal table state
    let page = 1;
    let sortColumn = "";
    let sortDirection = "asc";

    // Cache important DOM elements
    const dataUrl = container.dataset.url;
    const tbody = container.querySelector("tbody");
    const searchInput = container.querySelector(".snake-table-search");
    const pageSizeSelect = container.querySelector(".snake-table-page-size");
    const info = container.querySelector(".snake-table-info");
    const prevButton = container.querySelector(".snake-table-prev");
    const nextButton = container.querySelector(".snake-table-next");

    function enableSorting() {
        // Enable column sorting
        container.querySelectorAll("thead th").forEach((th) => {
            if (th.dataset.sortable !== "true") {
                return;
            }

            th.style.cursor = "pointer";

            th.addEventListener("click", (event) => {
                if (event.target.classList.contains("snake-table-resizer")) {
                    return;
                }

                const column = th.dataset.column;

                if (sortColumn === column) {
                    sortDirection = sortDirection === "asc" ? "desc" : "asc";
                } else {
                    sortColumn = column;
                    sortDirection = "asc";
                }

                page = 1;
                updateSortIndicators();
                loadTable();
            });
        });
    }

    function updateSortIndicators() {
        //  Update visual sort arrows

        container.querySelectorAll("thead th").forEach((th) => {
            const indicator = th.querySelector(".snake-table-sort-indicator");

            if (!indicator) {
                return;
            }

            if (th.dataset.column !== sortColumn) {
                indicator.textContent = "";
                return;
            }

            indicator.textContent = sortDirection === "asc" ? " ▲" : " ▼";
        });
    }

    async function loadTable() {
        // Load table data from the backend

        const params = new URLSearchParams({
            page: page,
            page_size: pageSizeSelect.value,
            search: searchInput.value,
            sort_column: sortColumn,
            sort_direction: sortDirection,
        });

        const langOf = container.dataset.langOf;
        const langClickToCopy = container.dataset.langClickToCopy;
        const updateUrl = container.dataset.updateUrl;

        const response = await fetch(`${dataUrl}?${params.toString()}`);
        const data = await response.json();

        tbody.innerHTML = "";

        const columns = getColumns(container);

        for (const row of data.rows) {
            const tr = document.createElement("tr");

            for (const column of columns) {
                const td = document.createElement("td");
                td.dataset.column = column.name;

                if (column.type === "select") {

                    td.innerHTML = `
                        <input
                            type="checkbox"
                            class="form-check-input"
                            data-id="${row.id}"
                        >
                    `;

                } else if (column.type === "checkbox") {

                    td.innerHTML = `
                        <input
                            type="checkbox"
                            class="form-check-input"
                            data-id="${row.id}"
                            data-column="${column.name}"
                            ${row[column.name] ? "checked" : ""}
                        >
                    `;

                    const checkbox = td.querySelector("input");

                    checkbox.addEventListener("change", async () => {
                        const response = await fetch(updateUrl, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            id: checkbox.dataset.id,
                            column: checkbox.dataset.column,
                            value: checkbox.checked,
                        }),
                    });
                });

                } else if (column.type === "link-button") {

                    const url = renderUrl(column.url, row);

                    td.innerHTML = `
                        <a href="${url}" class=" btn btn-sm btn-dark">
                            ${column.text || "Link"}
                        </a>
                    `;

                } else {

                    td.textContent = row[column.name] ?? "";

                    td.title = `${langClickToCopy}`;
                    td.classList.add("snake-table-copyable");

                    td.addEventListener("click", async () => {
                        const value = td.textContent.trim();

                        if (!value) {
                            return;
                        }

                        await navigator.clipboard.writeText(value);
                    });
                }

                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        const start = data.total === 0
            ? 0
            : ((data.page - 1) * data.page_size) + 1;

        const end = Math.min(data.page * data.page_size, data.total);

        info.textContent = `${start}-${end} ${langOf} ${data.total}`;

        prevButton.disabled = page <= 1;
        nextButton.disabled = end >= data.total;
    }

    searchInput.addEventListener("input", () => {
        page = 1;
        loadTable();
    });

    pageSizeSelect.addEventListener("change", () => {
        page = 1;
        loadTable();
    });

    prevButton.addEventListener("click", () => {
        if (page > 1) {
            page--;
            loadTable();
        }
    });

    nextButton.addEventListener("click", () => {
        page++;
        loadTable();
    });

    enableSorting();
    enableColumnResize(container);
    enableColumnDragDrop(container);

    loadTable();
}

function renderUrl(urlTemplate, row) {
    return urlTemplate.replace(
        /\{(.*?)\}/g,
        (_, field) => encodeURIComponent(row[field] ?? "")
    );
}

function enableColumnResize(container) {
    // Enable column resizing

    const table = container.querySelector("table");
    const headers = table.querySelectorAll("th");

    headers.forEach((th) => {
        const resizer = th.querySelector(".snake-table-resizer");

        if (!resizer) {
            return;
        }

        let startX = 0;
        let startWidth = 0;

        resizer.addEventListener("mousedown", (event) => {
            event.preventDefault();

            startX = event.pageX;
            startWidth = th.offsetWidth;

            document.addEventListener("mousemove", resizeColumn);
            document.addEventListener("mouseup", stopResize);
        });

        function resizeColumn(event) {
            const newWidth = startWidth + (event.pageX - startX);

            if (newWidth > 40) {
                th.style.width = `${newWidth}px`;
                th.style.minWidth = `${newWidth}px`;
                th.style.maxWidth = `${newWidth}px`;
            }
        }

        function stopResize() {
            document.removeEventListener("mousemove", resizeColumn);
            document.removeEventListener("mouseup", stopResize);
        }
    });
}

function enableColumnDragDrop(container) {
    // Enable drag-and-drop column reordering

    const table = container.querySelector("table");
    const headerRow = table.querySelector("thead tr");

    let draggedTh = null;
    let ghost = null;

    headerRow.querySelectorAll("th").forEach((th) => {
        th.addEventListener("dragstart", (event) => {
            draggedTh = th;
            th.classList.add("snake-table-dragging");

            ghost = document.createElement("div");
            ghost.className = "snake-table-drag-ghost";
            ghost.textContent = th.textContent.trim();
            document.body.appendChild(ghost);

            event.dataTransfer.setDragImage(ghost, 10, 10);
        });

        th.addEventListener("dragend", () => {
            th.classList.remove("snake-table-dragging");
            draggedTh = null;

            if (ghost) {
                ghost.remove();
                ghost = null;
            }
        });

        th.addEventListener("dragover", (event) => {
            event.preventDefault();

            const targetTh = event.currentTarget;

            if (!draggedTh || draggedTh === targetTh) {
                return;
            }

            const headers = [...headerRow.children];
            const draggedIndex = headers.indexOf(draggedTh);
            const targetIndex = headers.indexOf(targetTh);

            if (draggedIndex < targetIndex) {
                headerRow.insertBefore(draggedTh, targetTh.nextSibling);
            } else {
                headerRow.insertBefore(draggedTh, targetTh);
            }

            reorderBodyCells(container);
        });
    });
}

function reorderBodyCells(container) {
    // Reorder body cells to match header order

    const columnOrder = [...container.querySelectorAll("thead th")]
        .map(th => th.dataset.column);

    container.querySelectorAll("tbody tr").forEach((tr) => {
        const cells = [...tr.children];

        const cellsByColumn = {};

        cells.forEach((td) => {
            cellsByColumn[td.dataset.column] = td;
        });

        tr.innerHTML = "";

        columnOrder.forEach((columnName) => {
            if (cellsByColumn[columnName]) {
                tr.appendChild(cellsByColumn[columnName]);
            }
        });
    });
}
