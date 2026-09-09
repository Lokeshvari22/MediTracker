from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

from analytics.dashboard_metrics import DashboardMetrics


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


# ==================================
# Dashboard Page
# ==================================

@dashboard_bp.route("/")
@login_required
def dashboard():

    metrics = DashboardMetrics.get_dashboard_metrics(
        current_user.id
    )

    return render_template(
        "dashboard.html",
        metrics=metrics
    )


# ==================================
# Dashboard Charts API
# ==================================

@dashboard_bp.route("/api/dashboard/charts")
@login_required
def api_dashboard():

    charts = DashboardMetrics.chart_data(
        current_user.id
    )

    return jsonify({
        "category": charts["category"],
        "sales": charts["sales"]
    })