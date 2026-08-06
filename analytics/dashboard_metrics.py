from analytics.stock_analysis import StockAnalysis
from analytics.sales_analysis import SalesAnalysis
from analytics.expiry_analysis import ExpiryAnalysis


class DashboardMetrics:

    # ==================================
    # Dashboard Metrics
    # ==================================
    @staticmethod
    def get_dashboard_metrics(user_id):
        stock = StockAnalysis.summary(user_id) or {}
        sales = SalesAnalysis.statistics(user_id) or {}
        expiry = ExpiryAnalysis.summary(user_id) or {}

        return {
            # -------------------------
            # Inventory Cards (Template Aligned)
            # -------------------------
            "total_medicines": stock.get("total_stock", stock.get("total_medicines", 0)),
            "inventory_value": stock.get("inventory_value", 0.0),
            "low_stock": stock.get("low_stock", 0),
            "out_of_stock": stock.get("out_of_stock", 0),

            # -------------------------
            # Sales & Purchases
            # -------------------------
            "total_sales": sales.get("sales", 0.0),
            "total_purchases": sales.get("purchases", 0.0),
            "profit": sales.get("profit", 0.0),
            "sales_transactions": sales.get("transactions", 0),

            # -------------------------
            # Expiry Metrics (Template Aligned)
            # -------------------------
            "expired_medicines": expiry.get("expired", expiry.get("expired_medicines", 0)),
            "expiring_soon": expiry.get("expiring", expiry.get("expiring_soon", 0)),
            "expired_value": expiry.get("expired_value", 0.0),
            "expiring_value": expiry.get("expiring_value", 0.0),

            # -------------------------
            # Dashboard Table Data
            # -------------------------
            "low_stock_list": StockAnalysis.low_stock_items(user_id) if hasattr(StockAnalysis, 'low_stock_items') else [],
            "expiring_list": ExpiryAnalysis.expiring_soon(user_id, days=30) if hasattr(ExpiryAnalysis, 'expiring_soon') else [],
            "recent_sales": SalesAnalysis.recent_sales(user_id, limit=5) if hasattr(SalesAnalysis, 'recent_sales') else [],
            "recently_expired": ExpiryAnalysis.recently_expired(user_id, limit=5) if hasattr(ExpiryAnalysis, 'recently_expired') else []
        }

    # ==================================
    # Dashboard Charts
    # ==================================
    @staticmethod
    def chart_data(user_id):
        sales_dash = SalesAnalysis.dashboard(user_id) if hasattr(SalesAnalysis, 'dashboard') else {}
        sales_dash = sales_dash or {}
        categories = StockAnalysis.category_distribution(user_id) or []

        # Safe parsing for category list of dicts or dicts
        if isinstance(categories, list):
            category_labels = [item.get("category", "General") for item in categories]
            category_values = [item.get("count", 0) for item in categories]
        elif isinstance(categories, dict):
            category_labels = list(categories.keys())
            category_values = list(categories.values())
        else:
            category_labels, category_values = [], []

        return {
            "category": {
                "labels": category_labels,
                "values": category_values
            },
            "sales": {
                "labels": [item["month"] for item in sales_dash.get("monthly_sales", []) if "month" in item],
                "values": [item.get("sales", item.get("total", 0)) for item in sales_dash.get("monthly_sales", [])]
            },
            "purchases": {
                "labels": [item["month"] for item in sales_dash.get("monthly_purchases", []) if "month" in item],
                "values": [item.get("purchase", item.get("total", 0)) for item in sales_dash.get("monthly_purchases", [])]
            },
            "top_selling": sales_dash.get("top_selling", [])
        }

    # ==================================
    # Dashboard Summary
    # ==================================
    @staticmethod
    def summary(user_id):
        metrics = DashboardMetrics.get_dashboard_metrics(user_id)

        return {
            "inventory": {
                "stock": metrics["total_medicines"],
                "value": metrics["inventory_value"],
                "low_stock": metrics["low_stock"],
                "out_of_stock": metrics["out_of_stock"]
            },
            "sales": {
                "revenue": metrics["total_sales"],
                "purchases": metrics["total_purchases"],
                "profit": metrics["profit"]
            },
            "expiry": {
                "expired": metrics["expired_medicines"],
                "expiring": metrics["expiring_soon"],
                "expired_loss": metrics["expired_value"],
                "at_risk_value": metrics["expiring_value"]
            }
        }