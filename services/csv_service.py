import csv
import os
from datetime import datetime

from openpyxl import Workbook

from database.database import db

from models.medicine import Medicine
from models.transaction import Transaction

from services.inventory_service import InventoryService


class CSVService:

    # ==================================
    # Import Medicines CSV
    # ==================================

    @staticmethod
    def import_medicines(
        file_path,
        user_id
    ):

        imported = 0

        with open(
            file_path,
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                expiry_value = row.get("expiry_date", "")
                expiry_date = None
                if expiry_value:
                    expiry_date = datetime.strptime(expiry_value, "%Y-%m-%d").date()

                data = {

                    "name": row["name"],

                    "batch_number": row["batch_number"],

                    "category": row["category"],

                    "quantity": int(
                        row["quantity"]
                    ),

                    "price": float(
                        row["price"]
                    ),

                    "expiry_date": expiry_date,

                    "low_stock_alert": int(
                        row.get(
                            "low_stock_alert",
                            10
                        )
                    )

                }

                try:

                    InventoryService.add_medicine(
                        data,
                        user_id
                    )

                    imported += 1

                except Exception:

                    continue

        return imported

    # ==================================
    # Export Medicines CSV
    # ==================================

    @staticmethod
    def export_medicines_csv(
        user_id
    ):

        medicines = Medicine.query.filter_by(

            user_id=user_id

        ).order_by(

            Medicine.name.asc()

        ).all()

        filepath = os.path.join(

            "static",

            "uploads",

            "reports",

            "medicines.csv"

        )

        with open(

            filepath,

            "w",

            newline="",

            encoding="utf-8"

        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "ID",

                "Name",

                "Batch",

                "Category",

                "Quantity",

                "Price",

                "Expiry Date"

            ])

            for medicine in medicines:

                writer.writerow([

                    medicine.id,

                    medicine.name,

                    medicine.batch_number,

                    medicine.category,

                    medicine.quantity,

                    medicine.price,

                    medicine.expiry_date

                ])

        return filepath

    # ==================================
    # Export Medicines Excel
    # ==================================

    @staticmethod
    def export_medicines_excel(
        user_id
    ):

        medicines = Medicine.query.filter_by(

            user_id=user_id

        ).all()

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Medicines"

        sheet.append([

            "ID",

            "Name",

            "Batch",

            "Category",

            "Quantity",

            "Price",

            "Expiry"

        ])

        for medicine in medicines:

            sheet.append([

                medicine.id,

                medicine.name,

                medicine.batch_number,

                medicine.category,

                medicine.quantity,

                medicine.price,

                str(
                    medicine.expiry_date
                )

            ])

        filepath = os.path.join(

            "static",

            "uploads",

            "reports",

            "medicines.xlsx"

        )

        workbook.save(
            filepath
        )

        return filepath

    # ==================================
    # Export Transactions CSV
    # ==================================

    @staticmethod
    def export_transactions(
        user_id
    ):

        transactions = Transaction.query.filter_by(

            user_id=user_id

        ).order_by(

            Transaction.transaction_date.desc()

        ).all()

        filepath = os.path.join(

            "static",

            "uploads",

            "reports",

            "transactions.csv"

        )

        with open(

            filepath,

            "w",

            newline="",

            encoding="utf-8"

        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "ID",

                "Medicine",

                "Type",

                "Quantity",

                "Date"

            ])

            for transaction in transactions:

                writer.writerow([

                    transaction.id,

                    transaction.medicine.name,

                    transaction.transaction_type,

                    transaction.quantity,

                    transaction.transaction_date

                ])

        return filepath

    # ==================================
    # Export Transactions Excel
    # ==================================

    @staticmethod
    def export_transactions_excel(
        user_id
    ):

        transactions = Transaction.query.filter_by(

            user_id=user_id

        ).all()

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Transactions"

        sheet.append([

            "ID",

            "Medicine",

            "Type",

            "Quantity",

            "Date"

        ])

        for transaction in transactions:

            sheet.append([

                transaction.id,

                transaction.medicine.name,

                transaction.transaction_type,

                transaction.quantity,

                str(
                    transaction.transaction_date
                )

            ])

        filepath = os.path.join(

            "static",

            "uploads",

            "reports",

            "transactions.xlsx"

        )

        workbook.save(
            filepath
        )

        return filepath

    # ==================================
    # Export Dashboard Report CSV
    # ==================================

    @staticmethod
    def export_report(
        user_id,
        report_type="inventory",
        from_date=None,
        to_date=None
    ):

        # Map report types to specific exporters
        rt = (report_type or "").lower()

        from_date_obj = None
        to_date_obj = None
        if from_date:
            try:
                from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
            except Exception:
                pass
        if to_date:
            try:
                to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
            except Exception:
                pass

        if rt == "inventory":
            return CSVService.export_medicines_csv(user_id)

        if rt == "low_stock":
            from services.inventory_service import InventoryService
            medicines = InventoryService.low_stock(user_id)
            filepath = os.path.join("static", "uploads", "reports", "low_stock.csv")
            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Batch", "Category", "Quantity", "Price", "Expiry"])
                for med in medicines:
                    writer.writerow([
                        med.id,
                        med.name,
                        med.batch_number,
                        med.category,
                        med.quantity,
                        med.price,
                        med.expiry_date
                    ])
            return filepath

        if rt == "sales":
            from services.report_service import ReportService
            sales = ReportService.sales_report(user_id, from_date=from_date_obj, to_date=to_date_obj)

            filepath = os.path.join(
                "static",
                "uploads",
                "reports",
                "sales.csv"
            )

            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Invoice", "Customer", "Phone", "Medicine", "Qty", "Price", "Total", "Date"])
                for s in sales:
                    writer.writerow([
                        s.invoice_number or f"INV-{s.id}",
                        s.customer_name or "",
                        s.customer_phone or "",
                        s.medicine.name if s.medicine else "",
                        s.quantity,
                        s.sale_price,
                        s.total_amount,
                        s.sale_date
                    ])

            return filepath

        if rt == "purchase":
            from services.report_service import ReportService
            purchases = ReportService.purchase_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
            filepath = os.path.join("static", "uploads", "reports", "purchases.csv")
            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Invoice", "Supplier", "Medicine", "Qty", "Price", "Total", "Date"])
                for p in purchases:
                    writer.writerow([
                        p.invoice_number or f"PUR-{p.id}",
                        p.supplier.name if p.supplier else "",
                        p.medicine.name if p.medicine else "",
                        p.quantity,
                        p.purchase_price,
                        p.total_amount,
                        p.purchase_date
                    ])
            return filepath

        if rt == "expiry":
            from services.report_service import ReportService
            items = ReportService.expiry_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
            filepath = os.path.join("static", "uploads", "reports", "expired.csv")
            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Batch", "Qty", "Loss", "Expired On"])
                for it in items:
                    writer.writerow([it.id, it.name, it.batch_number, it.quantity, it.loss_amount, it.expiry_date or it.expired_date])
            return filepath

        # fallback to transactions
        return CSVService.export_transactions(user_id)

    # ==================================
    # Export Dashboard Report Excel
    # ==================================

    @staticmethod
    def export_report_excel(
        user_id,
        report_type="inventory",
        from_date=None,
        to_date=None
    ):

        rt = (report_type or "").lower()

        from_date_obj = None
        to_date_obj = None
        if from_date:
            try:
                from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
            except Exception:
                pass
        if to_date:
            try:
                to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
            except Exception:
                pass

        if rt == "inventory":
            return CSVService.export_medicines_excel(user_id)

        if rt == "sales":
            from services.report_service import ReportService
            sales = ReportService.sales_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Sales"
            sheet.append(["Invoice", "Customer", "Phone", "Medicine", "Qty", "Price", "Total", "Date"])
            for s in sales:
                sheet.append([
                    s.invoice_number or f"INV-{s.id}",
                    s.customer_name or "",
                    s.customer_phone or "",
                    s.medicine.name if s.medicine else "",
                    s.quantity,
                    s.sale_price,
                    s.total_amount,
                    str(s.sale_date)
                ])
            filepath = os.path.join("static", "uploads", "reports", "sales.xlsx")
            workbook.save(filepath)
            return filepath

        if rt == "purchase":
            from services.report_service import ReportService
            purchases = ReportService.purchase_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Purchases"
            sheet.append(["Invoice", "Supplier", "Medicine", "Qty", "Price", "Total", "Date"])
            for p in purchases:
                sheet.append([
                    p.invoice_number or f"PUR-{p.id}",
                    p.supplier.name if p.supplier else "",
                    p.medicine.name if p.medicine else "",
                    p.quantity,
                    p.purchase_price,
                    p.total_amount,
                    str(p.purchase_date)
                ])
            filepath = os.path.join("static", "uploads", "reports", "purchases.xlsx")
            workbook.save(filepath)
            return filepath

        if rt == "expiry":
            from services.report_service import ReportService
            items = ReportService.expiry_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Expired"
            sheet.append(["ID", "Name", "Batch", "Qty", "Loss", "Expired On"])
            for it in items:
                sheet.append([
                    it.id,
                    it.name,
                    it.batch_number,
                    it.quantity,
                    it.loss_amount,
                    str(it.expiry_date or it.expired_date)
                ])
            filepath = os.path.join("static", "uploads", "reports", "expired.xlsx")
            workbook.save(filepath)
            return filepath

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Transactions"
        sheet.append(["ID", "Medicine", "Type", "Quantity", "Date"])
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        for transaction in transactions:
            sheet.append([
                transaction.id,
                transaction.medicine.name if transaction.medicine else "",
                transaction.transaction_type,
                transaction.quantity,
                str(transaction.transaction_date)
            ])
        filepath = os.path.join("static", "uploads", "reports", "transactions.xlsx")
        workbook.save(filepath)
        return filepath