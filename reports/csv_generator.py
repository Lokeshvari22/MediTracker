"""
CSV Generator Module
Project: MediTracker

Generates tabular CSV files using standard library csv module.
"""

import csv


class CSVGenerator:

    @staticmethod
    def generate_inventory_csv(medicines, output_path):
        """
        Export inventory records to CSV.
        """
        fieldnames = ["ID", "Name", "Batch Number", "Category", "Quantity", "Price", "Expiry Date", "Low Stock Threshold"]

        with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for med in medicines:
                writer.writerow({
                    "ID": med.id,
                    "Name": med.name,
                    "Batch Number": med.batch_number,
                    "Category": med.category or "",
                    "Quantity": med.quantity,
                    "Price": med.price,
                    "Expiry Date": str(med.expiry_date) if med.expiry_date else "",
                    "Low Stock Threshold": med.low_stock_alert
                })

        return output_path

    @staticmethod
    def generate_sales_csv(sales, output_path):
        """
        Export sales history to CSV.
        """
        fieldnames = ["Invoice Number", "Customer Name", "Phone", "Medicine ID", "Quantity", "Sale Price", "Total Amount", "Sale Date"]

        with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for sale in sales:
                writer.writerow({
                    "Invoice Number": sale.invoice_number or f"INV-{sale.id}",
                    "Customer Name": sale.customer_name or "Walk-in",
                    "Phone": sale.customer_phone or "",
                    "Medicine ID": sale.medicine_id,
                    "Quantity": sale.quantity,
                    "Sale Price": sale.sale_price,
                    "Total Amount": sale.total_amount,
                    "Sale Date": sale.sale_date.strftime("%Y-%m-%d %H:%M:%S") if sale.sale_date else ""
                })

        return output_path

    @staticmethod
    def generate_suppliers_csv(suppliers, output_path):
        """
        Export suppliers directory to CSV.
        """
        fieldnames = ["ID", "Company Name", "Contact Person", "Phone", "Email", "Address"]

        with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for sup in suppliers:
                writer.writerow({
                    "ID": sup.id,
                    "Company Name": sup.name,
                    "Contact Person": sup.contact_person or "",
                    "Phone": sup.phone or "",
                    "Email": sup.email or "",
                    "Address": sup.address or ""
                })

        return output_path