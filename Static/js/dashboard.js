/**
 * MediTracker Dashboard
 * Chart.js Dashboard Controller
 */

document.addEventListener(
    "DOMContentLoaded",
    function () {
        loadDashboardCharts();
    }
);


const chartInstances = {};


/* ==========================================
   Load Dashboard Charts
========================================== */

async function loadDashboardCharts() {

    try {

        const response = await fetch(
            "/api/dashboard/charts",
            {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                `HTTP Error: ${response.status}`
            );
        }

        const data = await response.json();

        console.log(
            "Dashboard Chart Data:",
            data
        );

        createCategoryChart(
            data.category || {}
        );

        createSalesChart(
            data.sales || {}
        );

    } catch (error) {

        console.error(
            "Dashboard Analytics Error:",
            error
        );

        showEmptyCharts();
    }
}


/* ==========================================
   Category Doughnut Chart
========================================== */

function createCategoryChart(categoryData) {

    const canvas =
        document.getElementById(
            "categoryChart"
        );

    if (!canvas) {
        return;
    }

    const labels =
        categoryData.labels || [];

    const values =
        categoryData.values || [];

    if (
        labels.length === 0 ||
        values.length === 0
    ) {
        showEmptyCategory(canvas);
        return;
    }

    if (chartInstances.categoryChart) {

        chartInstances.categoryChart.destroy();
    }

    const ctx =
        canvas.getContext("2d");

    chartInstances.categoryChart =
        new Chart(ctx, {

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

                        borderColor:
                            "#ffffff",

                        hoverOffset: 6
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio:
                    false,

                plugins: {

                    legend: {

                        position:
                            "bottom",

                        labels: {

                            boxWidth: 12,

                            padding: 15
                        }
                    },

                    tooltip: {

                        callbacks: {

                            label:
                                function (
                                    context
                                ) {

                                    return (
                                        ` ${context.label}: ` +
                                        `${context.raw} Medicines`
                                    );
                                }
                        }
                    }
                }
            }
        });
}


/* ==========================================
   Monthly Sales Bar Chart
========================================== */

function createSalesChart(salesData) {

    const canvas =
        document.getElementById(
            "salesChart"
        );

    if (!canvas) {
        return;
    }

    const labels =
        salesData.labels || [];

    const values =
        salesData.values || [];

    if (
        labels.length === 0 ||
        values.length === 0
    ) {
        showEmptySales(canvas);
        return;
    }

    if (chartInstances.salesChart) {

        chartInstances.salesChart.destroy();
    }

    const ctx =
        canvas.getContext("2d");

    chartInstances.salesChart =
        new Chart(ctx, {

            type: "bar",

            data: {

                labels: labels,

                datasets: [
                    {
                        label:
                            "Monthly Revenue (₹)",

                        data: values,

                        backgroundColor:
                            "#198754",

                        borderColor:
                            "#198754",

                        borderWidth: 1,

                        borderRadius: 6,

                        borderSkipped:
                            false
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio:
                    false,

                plugins: {

                    legend: {

                        display: true,

                        position: "top"
                    },

                    tooltip: {

                        callbacks: {

                            label:
                                function (
                                    context
                                ) {

                                    const value =
                                        parseFloat(
                                            context.raw || 0
                                        );

                                    return (
                                        ` Revenue: ₹` +
                                        value.toFixed(2)
                                    );
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

                            callback:
                                function (
                                    value
                                ) {

                                    return (
                                        "₹ " +
                                        value
                                    );
                                }
                        }
                    }
                }
            }
        });
}


/* ==========================================
   Empty Category State
========================================== */

function showEmptyCategory(canvas) {

    if (
        !canvas ||
        !canvas.parentElement
    ) {
        return;
    }

    canvas.parentElement.innerHTML = `
        <div class="p-4 text-center text-muted">
            <i class="fa-solid fa-chart-pie fa-2x mb-2"></i>
            <p class="mb-0 small">
                No category data available.
            </p>
        </div>
    `;
}


/* ==========================================
   Empty Sales State
========================================== */

function showEmptySales(canvas) {

    if (
        !canvas ||
        !canvas.parentElement
    ) {
        return;
    }

    canvas.parentElement.innerHTML = `
        <div class="p-4 text-center text-muted">
            <i class="fa-solid fa-chart-bar fa-2x mb-2"></i>
            <p class="mb-0 small">
                No sales revenue data recorded.
            </p>
        </div>
    `;
}


/* ==========================================
   Empty Charts
========================================== */

function showEmptyCharts() {

    const category =
        document.getElementById(
            "categoryChart"
        );

    const sales =
        document.getElementById(
            "salesChart"
        );

    if (category) {
        showEmptyCategory(category);
    }

    if (sales) {
        showEmptySales(sales);
    }
}