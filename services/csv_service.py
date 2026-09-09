import csv
import os

from datetime import datetime

from openpyxl import Workbook

from database.database import db

from models.medicine import Medicine
from models.transaction import Transaction

from services.inventory_service import InventoryService


class CSVService:

    REQUIRED_HEADERS = {
        "name",
        "batch_number",
        "category",
        "quantity",
        "price",
        "expiry_date",
        "low_stock_alert"
    }

    REPORT_FOLDER = os.path.join(
        "static",
        "uploads",
        "reports"
    )

    # ==================================================
    # Create Report Folder
    # ==================================================

    @staticmethod
    def _ensure_report_folder():

        os.makedirs(
            CSVService.REPORT_FOLDER,
            exist_ok=True
        )

    # ==================================================
    # Import Medicines
    # ==================================================

    @staticmethod
    def import_medicines(
        file_path,
        user_id
    ):

        imported = 0
        skipped = 0
        errors = []

        with open(
            file_path,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:

                raise ValueError(
                    "CSV file is empty or has no headers."
                )

            headers = {
                h.strip()
                for h in reader.fieldnames
                if h
            }

            missing = (
                CSVService.REQUIRED_HEADERS
                - headers
            )

            if missing:

                raise ValueError(
                    "Missing required columns: "
                    + ", ".join(
                        sorted(missing)
                    )
                )

            for row_number, row in enumerate(
                reader,
                start=2
            ):

                try:

                    name = str(
                        row.get("name", "")
                    ).strip()

                    batch_number = str(
                        row.get(
                            "batch_number",
                            ""
                        )
                    ).strip()

                    category = str(
                        row.get(
                            "category",
                            ""
                        )
                    ).strip()

                    if not name:

                        raise ValueError(
                            "Medicine name is empty."
                        )

                    if not batch_number:

                        raise ValueError(
                            "Batch number is empty."
                        )

                    if not category:

                        raise ValueError(
                            "Category is empty."
                        )

                    # ----------------------------------
                    # Duplicate batch
                    # ----------------------------------

                    existing = Medicine.query.filter_by(
                        batch_number=batch_number,
                        user_id=user_id
                    ).first()

                    if existing:

                        skipped += 1
                        continue

                    # ----------------------------------
                    # Quantity
                    # ----------------------------------

                    quantity = int(
                        row.get(
                            "quantity",
                            0
                        )
                    )

                    if quantity < 0:

                        raise ValueError(
                            "Quantity cannot be negative."
                        )

                    # ----------------------------------
                    # Price
                    # ----------------------------------

                    price = float(
                        row.get(
                            "price",
                            0
                        )
                    )

                    if price < 0:

                        raise ValueError(
                            "Price cannot be negative."
                        )

                    # ----------------------------------
                    # Expiry
                    # ----------------------------------

                    expiry_value = str(
                        row.get(
                            "expiry_date",
                            ""
                        )
                    ).strip()

                    expiry_date = None

                    if expiry_value:

                        expiry_date = datetime.strptime(
                            expiry_value,
                            "%Y-%m-%d"
                        ).date()

                    # ----------------------------------
                    # Low stock
                    # ----------------------------------

                    alert_value = row.get(
                        "low_stock_alert",
                        10
                    )

                    if str(
                        alert_value
                    ).strip() == "":

                        alert_value = 10

                    low_stock_alert = int(
                        alert_value
                    )

                    if low_stock_alert < 1:

                        raise ValueError(
                            "Low stock alert must be at least 1."
                        )

                    data = {

                        "name": name,

                        "batch_number":
                            batch_number,

                        "category":
                            category,

                        "quantity":
                            quantity,

                        "price":
                            price,

                        "expiry_date":
                            expiry_date,

                        "low_stock_alert":
                            low_stock_alert
                    }

                    InventoryService.add_medicine(
                        data,
                        user_id
                    )

                    imported += 1

                except Exception as e:

                    db.session.rollback()

                    errors.append(
                        f"Row {row_number}: {e}"
                    )

        result = {
            "imported": imported,
            "skipped": skipped,
            "errors": errors
        }

        return result

    # ==================================================
    # Export Medicines CSV
    # ==================================================

    @staticmethod
    def export_medicines_csv(
        user_id,
        export_type="all"
    ):

        CSVService._ensure_report_folder()

        query = Medicine.query.filter_by(
            user_id=user_id
        )

        if export_type == "low_stock":

            query = query.filter(
                Medicine.quantity
                <= Medicine.low_stock_alert
            )

        medicines = query.order_by(
            Medicine.name.asc()
        ).all()

        filename = {
            "all":
                "medicines.csv",

            "low_stock":
                "low_stock_medicines.csv",

            "expired":
                "expired_medicines.csv"
        }.get(
            export_type,
            "medicines.csv"
        )

        if export_type == "expired":

            today = datetime.today().date()

            medicines = Medicine.query.filter(
                Medicine.user_id == user_id,
                Medicine.expiry_date < today
            ).order_by(
                Medicine.expiry_date.asc()
            ).all()

        filepath = os.path.join(
            CSVService.REPORT_FOLDER,
            filename
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
                "Expiry Date",
                "Low Stock Alert"
            ])

            for medicine in medicines:

                writer.writerow([
                    medicine.id,
                    medicine.name,
                    medicine.batch_number,
                    medicine.category,
                    medicine.quantity,
                    medicine.price,
                    medicine.expiry_date,
                    medicine.low_stock_alert
                ])

        return filepath

    # ==================================================
    # Export Medicines Excel
    # ==================================================

    @staticmethod
    def export_medicines_excel(
        user_id,
        export_type="all"
    ):

        CSVService._ensure_report_folder()

        query = Medicine.query.filter_by(
            user_id=user_id
        )

        if export_type == "low_stock":

            query = query.filter(
                Medicine.quantity
                <= Medicine.low_stock_alert
            )

        elif export_type == "expired":

            today = datetime.today().date()

            query = query.filter(
                Medicine.expiry_date < today
            )

        medicines = query.order_by(
            Medicine.name.asc()
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
            "Expiry Date",
            "Low Stock Alert"
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
                if medicine.expiry_date
                else "",
                medicine.low_stock_alert
            ])

        for column in sheet.columns:

            max_length = 0

            column_letter = column[0].column_letter

            for cell in column:

                value = str(
                    cell.value or ""
                )

                max_length = max(
                    max_length,
                    len(value)
                )

            sheet.column_dimensions[
                column_letter
            ].width = min(
                max_length + 2,
                40
            )

        filename = {
            "all":
                "medicines.xlsx",

            "low_stock":
                "low_stock_medicines.xlsx",

            "expired":
                "expired_medicines.xlsx"
        }.get(
            export_type,
            "medicines.xlsx"
        )

        filepath = os.path.join(
            CSVService.REPORT_FOLDER,
            filename
        )

        workbook.save(filepath)

        return filepath

    # ==================================================
    # Export Transactions CSV
    # ==================================================

    @staticmethod
    def export_transactions(
        user_id
    ):

        CSVService._ensure_report_folder()

        transactions = Transaction.query.filter_by(
            user_id=user_id
        ).order_by(
            Transaction.transaction_date.desc()
        ).all()

        filepath = os.path.join(
            CSVService.REPORT_FOLDER,
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
                    (
                        transaction.medicine.name
                        if transaction.medicine
                        else ""
                    ),
                    transaction.transaction_type,
                    transaction.quantity,
                    transaction.transaction_date
                ])

        return filepath

    # ==================================================
    # Export Transactions Excel
    # ==================================================

    @staticmethod
    def export_transactions_excel(
        user_id
    ):

        CSVService._ensure_report_folder()

        transactions = Transaction.query.filter_by(
            user_id=user_id
        ).order_by(
            Transaction.transaction_date.desc()
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
                (
                    transaction.medicine.name
                    if transaction.medicine
                    else ""
                ),
                transaction.transaction_type,
                transaction.quantity,
                str(
                    transaction.transaction_date
                )
            ])

        filepath = os.path.join(
            CSVService.REPORT_FOLDER,
            "transactions.xlsx"
        )

        workbook.save(filepath)

        return filepath