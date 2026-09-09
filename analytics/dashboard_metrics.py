from analytics.stock_analysis import StockAnalysis
from analytics.sales_analysis import SalesAnalysis
from analytics.expiry_analysis import ExpiryAnalysis


class DashboardMetrics:

    # ==================================
    # Dashboard Metrics
    # ==================================

    @staticmethod
    def get_dashboard_metrics(user_id):

        stock = StockAnalysis.summary(
            user_id
        ) or {}

        expiry = ExpiryAnalysis.summary(
            user_id
        ) or {}

        return {

            # -------------------------
            # Dashboard Cards
            # -------------------------

            "total_medicines":
                stock.get(
                    "total_medicines",
                    0
                ),

            "low_stock":
                stock.get(
                    "low_stock",
                    0
                ),

            "expired_medicines":
                expiry.get(
                    "expired",
                    0
                ),

            "expiring_soon":
                expiry.get(
                    "expiring",
                    0
                ),

            "inventory_value":
                stock.get(
                    "inventory_value",
                    0.0
                ),

            # -------------------------
            # Dashboard Tables
            # -------------------------

            "low_stock_list":
                StockAnalysis.low_stock_items(
                    user_id
                ),

            "expiring_list":
                ExpiryAnalysis.expiring_soon(
                    user_id,
                    days=30
                ),

            "recently_expired":
                ExpiryAnalysis.recently_expired(
                    user_id,
                    limit=5
                )
        }

    # ==================================
    # Dashboard Charts
    # ==================================

    @staticmethod
    def chart_data(user_id):

        sales_dash = SalesAnalysis.dashboard(user_id) or {}
        categories = StockAnalysis.category_distribution(user_id) or []

        if isinstance(categories, list):
            category_labels = [
                item.get("category", "General")
                for item in categories
            ]

            category_values = [
                item.get("count", 0)
                for item in categories
            ]

        elif isinstance(categories, dict):
            category_labels = list(categories.keys())
            category_values = list(categories.values())

        else:
            category_labels = []
            category_values = []

        return {
            "category": {
                "labels": category_labels,
                "values": category_values
            },

            "sales": {
                "labels": [
                    item["month"]
                    for item in sales_dash.get("monthly_sales", [])
                    if item.get("month")
                ],

                "values": [
                    item.get("sales", 0)
                    for item in sales_dash.get("monthly_sales", [])
                ]
            }
        }
    # ==================================
    # Optional Summary
    # ==================================

    @staticmethod
    def summary(user_id):

        metrics = (
            DashboardMetrics
            .get_dashboard_metrics(user_id)
        )

        return {

            "inventory": {
                "medicines":
                    metrics["total_medicines"],

                "value":
                    metrics["inventory_value"],

                "low_stock":
                    metrics["low_stock"]
            },

            "expiry": {
                "expired":
                    metrics["expired_medicines"],

                "expiring":
                    metrics["expiring_soon"]
            }
        }