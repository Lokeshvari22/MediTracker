/**
 * MediTracker Reports Controller
 * Handles report data fetching, table population, and dynamic file exports
 */

document.addEventListener("DOMContentLoaded", function () {
    loadReports();
});

/**
 * Fetch and populate all summary reports
 */
async function loadReports() {
    try {
        const response = await fetch("/api/reports");

        if (!response.ok) {
            throw new Error(`Failed to load reports (Status: ${response.status})`);
        }

        const data = await response.json();

        updateSalesReport(data.sales || []);
        updateInventoryReport(data.inventory || {});
        updateExpiryReport(data.expiry || []);

    } catch (error) {
        console.error("Report loading error:", error);
        showReportError("Unable to load reports. Please try refreshing the page.");
    }
}

/**
 * Populate Sales Report Table
 */
function updateSalesReport(salesData) {
    const tableBody = document.getElementById("sales-report-body");

    if (!tableBody) return;

    tableBody.innerHTML = "";

    if (!salesData || salesData.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-3">
                    <i class="fa-solid fa-receipt me-1"></i> No sales records found.
                </td>
            </tr>
        `;
        return;
    }

    salesData.forEach(item => {
        const row = document.createElement("tr");

        const medName = item.medicine || item.name || "N/A";
        const quantity = item.quantity || 0;
        const total = item.total || item.total_amount || 0;
        const dateVal = item.date || item.sale_date || "N/A";

        row.innerHTML = `
            <td class="fw-semibold text-dark">${escapeHtml(medName)}</td>
            <td class="text-center">${quantity}</td>
            <td class="fw-bold text-success">₹ ${parseFloat(total).toFixed(2)}</td>
            <td class="text-muted small">${escapeHtml(dateVal)}</td>
        `;

        tableBody.appendChild(row);
    });
}

/**
 * Update Inventory Summary Metrics
 */
function updateInventoryReport(inventoryData) {
    const totalElement = document.getElementById("inventory-count");
    if (totalElement) {
        totalElement.innerText = inventoryData.total || inventoryData.total_medicines || 0;
    }

    const lowStockElement = document.getElementById("low-stock-count");
    if (lowStockElement) {
        lowStockElement.innerText = inventoryData.low_stock || inventoryData.low_stock_count || 0;
    }

    const valueElement = document.getElementById("inventory-value");
    if (valueElement) {
        const val = inventoryData.value || inventoryData.total_value || 0;
        valueElement.innerText = "₹ " + parseFloat(val).toFixed(2);
    }
}

/**
 * Populate Expiry Audit Table
 */
function updateExpiryReport(expiryData) {
    const expiryTable = document.getElementById("expiry-report-body");

    if (!expiryTable) return;

    expiryTable.innerHTML = "";

    if (!expiryData || expiryData.length === 0) {
        expiryTable.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-3">
                    <i class="fa-solid fa-circle-check me-1 text-success"></i> No medicines nearing expiration.
                </td>
            </tr>
        `;
        return;
    }

    expiryData.forEach(medicine => {
        const row = document.createElement("tr");

        const name = medicine.name || medicine.medicine || "N/A";
        const batch = medicine.batch || medicine.batch_number || "N/A";
        const expDate = medicine.expiry_date || "N/A";
        const status = medicine.status || (medicine.is_expired ? "Expired" : "Expiring Soon");

        // Contextual Badge Class
        let badgeClass = "badge bg-warning text-dark";
        if (status.toLowerCase().includes("expired")) {
            badgeClass = "badge bg-danger";
        } else if (status.toLowerCase().includes("safe") || status.toLowerCase().includes("active")) {
            badgeClass = "badge bg-success";
        }

        row.innerHTML = `
            <td class="fw-semibold text-dark">${escapeHtml(name)}</td>
            <td><code>${escapeHtml(batch)}</code></td>
            <td>${escapeHtml(expDate)}</td>
            <td>
                <span class="${badgeClass}">
                    ${escapeHtml(status)}
                </span>
            </td>
        `;

        expiryTable.appendChild(row);
    });
}

/**
 * Trigger File Export with active filters
 */
function exportReport(type, format = "csv") {
    const fromDate = document.querySelector("input[name='from_date']")?.value || "";
    const toDate = document.querySelector("input[name='to_date']")?.value || "";

    let exportUrl = `/reports/export/${type}?format=${format}`;

    if (fromDate) exportUrl += `&from_date=${encodeURIComponent(fromDate)}`;
    if (toDate) exportUrl += `&to_date=${encodeURIComponent(toDate)}`;

    window.location.href = exportUrl;
}

/**
 * Display Alert Banner on Error
 */
function showReportError(message) {
    const alertBox = document.getElementById("report-alert");

    if (alertBox) {
        alertBox.innerText = message;
        alertBox.className = "alert alert-danger alert-dismissible fade show mt-3 mb-0";
        alertBox.style.display = "block";
    } else {
        console.warn("Report Error:", message);
    }
}

/**
 * Safe HTML string escaping
 */
function escapeHtml(str) {
    if (typeof str !== "string") return str;
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}