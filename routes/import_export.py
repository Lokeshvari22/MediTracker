from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

import os

from config import Config
from services.csv_service import CSVService


import_export_bp = Blueprint(
    "import_export",
    __name__,
    url_prefix="/import-export"
)


# ==========================================================
# Import Medicines from CSV
# ==========================================================

@import_export_bp.route(
    "/import",
    methods=["GET", "POST"]
)
@login_required
def import_csv():

    if request.method == "POST":

        if "file" not in request.files and "csv_file" not in request.files:

            flash(
                "No file selected.",
                "danger"
            )

            return redirect(request.url)

        file = request.files.get("file") or request.files.get("csv_file")

        if not file or file.filename == "":

            flash(
                "Please choose a CSV file.",
                "warning"
            )

            return redirect(request.url)

        filename = secure_filename(
            file.filename
        )

        upload_path = os.path.join(
            Config.UPLOAD_FOLDER,
            "csv",
            filename
        )

        file.save(upload_path)

        try:

            imported = CSVService.import_medicines(
                file_path=upload_path,
                user_id=current_user.id
            )

            flash(
                f"{imported} medicines imported successfully.",
                "success"
            )

        except Exception as e:

            flash(
                f"Import failed: {e}",
                "danger"
            )

        return redirect(
            url_for(
                "medicine.medicines"
            )
        )

    return render_template(
        "medicines/import_csv.html"
    )


# ==========================================================
# Export Medicines CSV
# ==========================================================

@import_export_bp.route("/export/csv")
@login_required
def export_csv():

    filepath = CSVService.export_medicines_csv(
        current_user.id
    )

    return send_file(
        filepath,
        as_attachment=True
    )


# ==========================================================
# Export Medicines Excel
# ==========================================================

@import_export_bp.route("/export/excel")
@login_required
def export_excel():

    filepath = CSVService.export_medicines_excel(
        current_user.id
    )

    return send_file(
        filepath,
        as_attachment=True
    )


# ==========================================================
# Download Sample CSV
# ==========================================================

@import_export_bp.route("/sample")
@login_required
def download_sample():

    sample = os.path.join(
        "sample_data",
        "medicines.csv"
    )

    return send_file(
        sample,
        as_attachment=True
    )