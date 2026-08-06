/**
 * MediTracker Dashboard Controller
 * Handles live analytics fetching and Chart.js dynamic rendering.
 */

document.addEventListener("DOMContentLoaded", function () {
    loadDashboardCharts();
});

// Chart instances store to prevent canvas reuse errors
const chartInstances = {};

async function loadDashboardCharts() {
    try {
        const response = await fetch("/api/dashboard/charts");

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        createCategoryChart(data.category_chart || data.categories || []);
        createSalesChart(data.monthly_sales || data.sales || []);
    } catch (error) {
        console.error("Dashboard Analytics Fetch Error:", error);
        showEmptyCharts();
    }
}

/* ===========================================
   Category Distribution Doughnut Chart
=========================================== */
function createCategoryChart(categoryData) {
    const canvas = document.getElementById("categoryChart");
    if (!canvas) return;

    if (!categoryData || categoryData.length === 0) {
        showEmptyCategory(canvas);
        return;
    }

    const labels = categoryData.map(item => item.category || item.name || "General");
    const values = categoryData.map(item => item.count || item.total || item.quantity || 0);

    // Destroy existing instance if present
    if (chartInstances.categoryChart) {
        chartInstances.categoryChart.destroy();
    }

    const ctx = canvas.getContext("2d");

    chartInstances.categoryChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [
                {
                    data: values,
                    backgroundColor: [
                        "#198754",
                        "#0d6efd",
                        "#ffc107",
                        "#dc3545",
                        "#20c997",
                        "#0dcaf0",
                        "#6f42c1",
                        "#fd7e14"
                    ],
                    borderWidth: 2,
                    borderColor: "#ffffff",
                    hoverOffset: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        font: {
                            family: "'Segoe UI', sans-serif",
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return ` ${context.label}: ${context.raw} Items`;
                        }
                    }
                }
            }
        }
    });
}

/* ===========================================
   Monthly Sales Bar Chart
=========================================== */
function createSalesChart(monthlySales) {
    const canvas = document.getElementById("salesChart");
    if (!canvas) return;

    if (!monthlySales || monthlySales.length === 0) {
        showEmptySales(canvas);
        return;
    }

    const labels = monthlySales.map(item => item.month || item.name || "N/A");
    const values = monthlySales.map(item => item.total || item.sales || item.amount || 0);

    // Destroy existing instance if present
    if (chartInstances.salesChart) {
        chartInstances.salesChart.destroy();
    }

    const ctx = canvas.getContext("2d");

    // Optional gradient fill for sales bars
    let gradient = "#198754";
    if (ctx) {
        gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, "rgba(25, 135, 84, 0.85)");
        gradient.addColorStop(1, "rgba(25, 135, 84, 0.2)");
    }

    chartInstances.salesChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Monthly Revenue (₹)",
                    data: values,
                    backgroundColor: gradient,
                    borderColor: "#198754",
                    borderWidth: 1.5,
                    borderRadius: 6,
                    borderSkipped: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "top"
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return ` Revenue: ₹${parseFloat(context.raw).toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return "₹ " + value;
                        }
                    }
                }
            }
        }
    });
}

/* ===========================================
   Empty Chart State Fallbacks
=========================================== */
function showEmptyCategory(canvas) {
    if (!canvas || !canvas.parentElement) return;
    canvas.parentElement.innerHTML =
        "<div class='p-4 text-center text-muted'><i class='fa-solid fa-chart-pie fa-2x mb-2 text-secondary'></i><p class='mb-0 small'>No category data available to plot.</p></div>";
}

function showEmptySales(canvas) {
    if (!canvas || !canvas.parentElement) return;
    canvas.parentElement.innerHTML =
        "<div class='p-4 text-center text-muted'><i class='fa-solid fa-chart-bar fa-2x mb-2 text-secondary'></i><p class='mb-0 small'>No sales revenue data recorded.</p></div>";
}

function showEmptyCharts() {
    const category = document.getElementById("categoryChart");
    const sales = document.getElementById("salesChart");

    if (category) {
        showEmptyCategory(category);
    }
    if (sales) {
        showEmptySales(sales);
    }
}