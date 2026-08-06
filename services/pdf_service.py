import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from models.medicine import Medicine
from models.transaction import Transaction
from models.sale import Sale


class PDFService:

    # ==================================
    # Export Medicines PDF
    # ==================================

    @staticmethod
    def export_medicines(user_id):

        medicines = Medicine.query.filter_by(
            user_id=user_id
        ).order_by(
            Medicine.name.asc()
        ).all()

        filepath = os.path.join(
            "static",
            "uploads",
            "reports",
            "medicines.pdf"
        )

        styles = getSampleStyleSheet()

        document = SimpleDocTemplate(
            filepath
        )

        elements = []

        elements.append(
            Paragraph(
                "Medicine Inventory Report",
                styles["Heading1"]
            )
        )

        data = [[
            "ID",
            "Name",
            "Batch",
            "Category",
            "Qty",
            "Price",
            "Expiry"
        ]]

        for medicine in medicines:

            data.append([

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

        table = Table(data)

        table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.grey
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.whitesmoke
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.beige
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                )

            ])

        )

        elements.append(table)

        document.build(elements)

        return filepath

    # ==================================
    # Export Transactions PDF
    # ==================================

    @staticmethod
    def export_transactions(user_id):

        transactions = Transaction.query.filter_by(
            user_id=user_id
        ).order_by(
            Transaction.transaction_date.desc()
        ).all()

        filepath = os.path.join(
            "static",
            "uploads",
            "reports",
            "transactions.pdf"
        )

        styles = getSampleStyleSheet()

        document = SimpleDocTemplate(
            filepath
        )

        elements = []

        elements.append(
            Paragraph(
                "Transaction Report",
                styles["Heading1"]
            )
        )

        data = [[
            "ID",
            "Medicine",
            "Type",
            "Quantity",
            "Date"
        ]]

        for transaction in transactions:

            data.append([

                transaction.id,

                transaction.medicine.name,

                transaction.transaction_type,

                transaction.quantity,

                str(
                    transaction.transaction_date
                )

            ])

        table = Table(data)

        table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.darkblue
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.lightgrey
                )

            ])

        )

        elements.append(table)

        document.build(elements)

        return filepath

    # ==================================
    # Export Sales Invoice
    # ==================================

    @staticmethod
    def generate_invoice(sale_id):

        sale = Sale.query.get_or_404(
            sale_id
        )

        filepath = os.path.join(
            "static",
            "uploads",
            "invoices",
            f"invoice_{sale.id}.pdf"
        )

        styles = getSampleStyleSheet()

        document = SimpleDocTemplate(
            filepath
        )

        elements = []

        elements.append(

            Paragraph(
                "Medicine Invoice",
                styles["Heading1"]
            )

        )

        elements.append(

            Paragraph(
                f"Invoice No : {sale.id}",
                styles["Normal"]
            )

        )

        elements.append(

            Paragraph(
                f"Customer : {sale.customer_name}",
                styles["Normal"]
            )

        )

        elements.append(

            Paragraph(
                f"Medicine : {sale.medicine.name}",
                styles["Normal"]
            )

        )

        elements.append(

            Paragraph(
                f"Quantity : {sale.quantity}",
                styles["Normal"]
            )

        )

        elements.append(

            Paragraph(
                f"Price : ₹{sale.selling_price}",
                styles["Normal"]
            )

        )

        elements.append(

            Paragraph(
                f"Total : ₹{sale.total_amount}",
                styles["Heading2"]
            )

        )

        document.build(elements)

        return filepath

    # ==================================
    # Export Report PDF
    # ==================================

    @staticmethod
    def export_report(user_id, report_type="inventory", from_date=None, to_date=None):

        rt = (report_type or "").lower()
        from_date_obj = None
        to_date_obj = None

        if from_date:
            try:
                from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            except Exception:
                pass

        if to_date:
            try:
                to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            except Exception:
                pass

        if rt == "inventory":
            return PDFService.export_medicines(user_id)

        if rt == "low_stock":
            from services.inventory_service import InventoryService
            medicines = InventoryService.low_stock(user_id)
            filepath = os.path.join("static", "uploads", "reports", "low_stock.pdf")
            styles = getSampleStyleSheet()
            document = SimpleDocTemplate(filepath)
            elements = [Paragraph("Low Stock Medicine Report", styles["Heading1"])]
            data = [["ID", "Name", "Batch", "Category", "Qty", "Price", "Expiry"]]
            for med in medicines:
                data.append([
                    med.id,
                    med.name,
                    med.batch_number,
                    med.category,
                    med.quantity,
                    med.price,
                    str(med.expiry_date)
                ])
            table = Table(data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("ALIGN", (0, 0), (-1, -1), "CENTER")
            ]))
            elements.append(table)
            document.build(elements)
            return filepath

        if rt in ["sales", "purchase", "expiry"]:
            from services.report_service import ReportService
            if rt == "sales":
                items = ReportService.sales_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
                title = "Sales Report"
                headers = ["Invoice", "Customer", "Phone", "Medicine", "Qty", "Price", "Total", "Date"]
                rows = [
                    [
                        s.invoice_number or f"INV-{s.id}",
                        s.customer_name or "",
                        s.customer_phone or "",
                        s.medicine.name if s.medicine else "",
                        s.quantity,
                        s.sale_price,
                        s.total_amount,
                        str(s.sale_date)
                    ]
                    for s in items
                ]
                filename = "sales.pdf"
            elif rt == "purchase":
                items = ReportService.purchase_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
                title = "Purchase Report"
                headers = ["Invoice", "Supplier", "Medicine", "Qty", "Price", "Total", "Date"]
                rows = [
                    [
                        p.invoice_number or f"PUR-{p.id}",
                        p.supplier.name if p.supplier else "",
                        p.medicine.name if p.medicine else "",
                        p.quantity,
                        p.purchase_price,
                        p.total_amount,
                        str(p.purchase_date)
                    ]
                    for p in items
                ]
                filename = "purchases.pdf"
            else:
                items = ReportService.expiry_report(user_id, from_date=from_date_obj, to_date=to_date_obj)
                title = "Expiry Audit Report"
                headers = ["ID", "Name", "Batch", "Qty", "Loss", "Expired On"]
                rows = [
                    [
                        it.id,
                        it.name,
                        it.batch_number,
                        it.quantity,
                        it.loss_amount,
                        str(it.expiry_date or it.expired_date)
                    ]
                    for it in items
                ]
                filename = "expired.pdf"

            filepath = os.path.join("static", "uploads", "reports", filename)
            styles = getSampleStyleSheet()
            document = SimpleDocTemplate(filepath)
            elements = [Paragraph(title, styles["Heading1"])]
            data = [headers] + rows
            table = Table(data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("ALIGN", (0, 0), (-1, -1), "CENTER")
            ]))
            elements.append(table)
            document.build(elements)
            return filepath

        return PDFService.export_transactions(user_id)