# In routes/dashboard.py
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from analytics.dashboard_metrics import DashboardMetrics

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def dashboard():
    """Renders main dashboard HTML."""
    metrics = DashboardMetrics.get_dashboard_metrics(current_user.id)
    return render_template("dashboard.html", metrics=metrics)


@dashboard_bp.route("/api/dashboard/charts")
@login_required
def api_dashboard():
    """Provides Chart.js JSON data for dashboard.js."""
    charts = DashboardMetrics.chart_data(current_user.id)

    # Format category data for dashboard.js expectations
    category_chart = [
        {"category": label, "count": val}
        for label, val in zip(charts["category"]["labels"], charts["category"]["values"])
    ]

    # Format sales data for dashboard.js expectations
    monthly_sales = [
        {"month": label, "total": val}
        for label, val in zip(charts["sales"]["labels"], charts["sales"]["values"])
    ]

    return jsonify({
        "category_chart": category_chart,
        "monthly_sales": monthly_sales
    })