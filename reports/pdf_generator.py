"""
PDF Generator Module
Project: MediTracker

Generates PDF reports for:
- Inventory status
- Sales summary
- Purchase records
- Expired / Expiring medicines
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


class PDFGenerator:

    @staticmethod
    def generate_inventory_pdf(medicines, output_path):
        """
        Generates a PDF report for current medicine inventory.
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        elements = []
        styles = getSampleStyleSheet()

        # Custom Title Style
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10
        )

        subtitle_style = ParagraphStyle(
            'ReportSubTitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=20
        )

        # Title Block
        elements.append(Paragraph("MediTracker - Inventory Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))

        # Table Data Construction
        table_data = [["ID", "Name", "Batch No", "Category", "Quantity", "Price (₹)", "Expiry Date"]]

        for med in medicines:
            table_data.append([
                str(med.id),
                med.name,
                med.batch_number,
                med.category or "N/A",
                str(med.quantity),
                f"{med.price:.2f}",
                str(med.expiry_date) if med.expiry_date else "N/A"
            ])

        # Table Styling
        t = Table(table_data, colWidths=[30, 140, 75, 80, 55, 65, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#212529')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))

        elements.append(t)
        doc.build(elements)
        return output_path

    @staticmethod
    def generate_sales_pdf(sales, output_path):
        """
        Generates a PDF report for sales history.
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("MediTracker - Sales Report", styles['Heading1']))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 15))

        table_data = [["Invoice", "Customer", "Medicine", "Qty", "Price", "Total (₹)", "Date"]]

        for sale in sales:
            table_data.append([
                sale.invoice_number or f"INV-{sale.id}",
                sale.customer_name or "Walk-in",
                sale.medicine.name if sale.medicine else "N/A",
                str(sale.quantity),
                f"{sale.sale_price:.2f}",
                f"{sale.total_amount:.2f}",
                sale.sale_date.strftime("%Y-%m-%d") if sale.sale_date else "N/A"
            ])

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ]))

        elements.append(t)
        doc.build(elements)
        return output_path