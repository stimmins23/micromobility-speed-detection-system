const API_BASE_URL = "";
const EVENTS_ENDPOINT = "/events";

document.addEventListener("DOMContentLoaded", () => {
    loadEvents();

    const refreshButton = document.querySelector("#refreshButton");
    if (refreshButton) {
        refreshButton.addEventListener("click", loadEvents);
    }
});

async function loadEvents() {
    try {
        showLoadingState();

        const response = await fetch(`${API_BASE_URL}${EVENTS_ENDPOINT}`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const events = await response.json();

        updateSummaryCards(events);
        renderEventsTable(events);
    } catch (error) {
        console.error("Error loading events:", error);
        showErrorState("Failed to load speed events from the API.");
    }
}

function updateSummaryCards(events) {
    const totalEvents = events.length;

    const violations = events.filter(event =>
        event.speed_mph > event.threshold_value
    ).length;

    const avgSpeed = totalEvents > 0
        ? (events.reduce((sum, event) => sum + event.speed_mph, 0) / totalEvents).toFixed(1)
        : "0.0";

    const highestSpeed = totalEvents > 0
        ? Math.max(...events.map(event => event.speed_mph)).toFixed(1)
        : "0.0";

    const summaryValues = document.querySelectorAll(".summary-value");

    if (summaryValues.length >= 4) {
        summaryValues[0].textContent = totalEvents;
        summaryValues[1].textContent = violations;
        summaryValues[2].textContent = `${avgSpeed} mph`;
        summaryValues[3].textContent = `${highestSpeed} mph`;
    }
}

function renderEventsTable(events) {
    const tableBody = document.querySelector("#eventsTableBody");

    if (!tableBody) return;

    tableBody.innerHTML = "";

    if (events.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted">
                    No events found.
                </td>
            </tr>
        `;
        return;
    }

    events.forEach(event => {
        const row = document.createElement("tr");

        const formattedTimestamp = formatDateTime(event.timestamp);

        const imageCell = event.image_paths && event.image_paths.length > 0
            ? `
                <div class="d-flex flex-wrap gap-2">
                    ${event.image_paths.map(path => `
                        <img
                            src="/captures/${path}"
                            alt="Event image"
                            class="img-thumbnail"
                            style="width: 120px; height: 90px; object-fit: cover;"
                        >
                    `).join("")}
                </div>
            `
            : `<span class="text-muted">No Images</span>`;

        const exceeded = event.speed_mph > event.threshold_value
            ? `<span class="badge bg-danger">Yes</span>`
            : `<span class="badge bg-success">No</span>`;

        row.innerHTML = `
            <td>${event.id}</td>
            <td>${formattedTimestamp}</td>
            <td>${event.speed_mph.toFixed(1)} mph</td>
            <td>${event.threshold_value.toFixed(1)} mph</td>
            <td>${event.location || "Unknown"}</td>
            <td>${imageCell}</td>
            <td>${exceeded}</td>
        `;

        tableBody.appendChild(row);
    });
}

function formatDateTime(timestamp) {
    const date = new Date(timestamp);
    return isNaN(date.getTime()) ? timestamp : date.toLocaleString();
}

function showLoadingState() {
    const tableBody = document.querySelector("#eventsTableBody");

    if (tableBody) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted">
                    Loading events...
                </td>
            </tr>
        `;
    }
}

function showErrorState(message) {
    const tableBody = document.querySelector("#eventsTableBody");

    if (tableBody) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-danger">
                    ${message}
                </td>
            </tr>
        `;
    }
}