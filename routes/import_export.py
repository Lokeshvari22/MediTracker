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
# Import Medicines
# ==========================================================

@import_export_bp.route(
    "/import",
    methods=["GET", "POST"]
)
@login_required
def import_csv():

    if request.method == "POST":

        if (
            "file" not in request.files
            and
            "csv_file" not in request.files
        ):

            flash(
                "No file selected.",
                "danger"
            )

            return redirect(
                request.url
            )

        file = (
            request.files.get("file")
            or request.files.get("csv_file")
        )

        if not file or not file.filename:

            flash(
                "Please choose a CSV file.",
                "warning"
            )

            return redirect(
                request.url
            )

        filename = secure_filename(
            file.filename
        )

        if not filename.lower().endswith(
            ".csv"
        ):

            flash(
                "Only CSV files are supported.",
                "danger"
            )

            return redirect(
                request.url
            )

        upload_folder = os.path.join(
            Config.UPLOAD_FOLDER,
            "csv"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        upload_path = os.path.join(
            upload_folder,
            filename
        )

        try:

            file.save(upload_path)

            result = CSVService.import_medicines(
                file_path=upload_path,
                user_id=current_user.id
            )

            imported = result["imported"]
            skipped = result["skipped"]
            errors = result["errors"]

            if imported:

                flash(
                    f"{imported} medicines "
                    "imported successfully.",
                    "success"
                )

            if skipped:

                flash(
                    f"{skipped} duplicate medicines "
                    "were skipped.",
                    "warning"
                )

            if errors:

                preview = errors[:5]

                message = (
                    "Some rows could not be imported: "
                    + " | ".join(preview)
                )

                if len(errors) > 5:

                    message += (
                        f" | And {len(errors) - 5} "
                        "more error(s)."
                    )

                flash(
                    message,
                    "danger"
                )

        except Exception as e:

            flash(
                f"Import failed: {e}",
                "danger"
            )

        finally:

            if os.path.exists(upload_path):

                try:
                    os.remove(upload_path)
                except OSError:
                    pass

        return redirect(
            url_for(
                "medicine.medicines"
            )
        )

    return render_template(
        "medicines/import_csv.html"
    )


# ==========================================================
# Export Data
# ==========================================================

@import_export_bp.route(
    "/export",
    methods=["GET", "POST"]
)
@login_required
def export_data():

    if request.method == "GET":

        return render_template(
            "medicines/export.html"
        )

    export_format = request.form.get(
        "format",
        "csv"
    ).lower()

    export_type = request.form.get(
        "export_type",
        "all"
    ).lower()

    if export_type not in {
        "all",
        "low_stock",
        "expired"
    }:

        export_type = "all"

    try:

        if export_format == "csv":

            filepath = (
                CSVService.export_medicines_csv(
                    current_user.id,
                    export_type
                )
            )

        elif export_format == "excel":

            filepath = (
                CSVService.export_medicines_excel(
                    current_user.id,
                    export_type
                )
            )

        elif export_format == "pdf":

            flash(
                "PDF export is not implemented yet.",
                "warning"
            )

            return redirect(
                url_for(
                    "import_export.export_data"
                )
            )

        else:

            flash(
                "Invalid export format.",
                "danger"
            )

            return redirect(
                url_for(
                    "import_export.export_data"
                )
            )

        return send_file(
            filepath,
            as_attachment=True
        )

    except Exception as e:

        flash(
            f"Export failed: {e}",
            "danger"
        )

        return redirect(
            url_for(
                "import_export.export_data"
            )
        )


# ==========================================================
# Direct CSV Export
# ==========================================================

@import_export_bp.route(
    "/export/csv"
)
@login_required
def export_csv():

    filepath = CSVService.export_medicines_csv(
        current_user.id,
        "all"
    )

    return send_file(
        filepath,
        as_attachment=True
    )


# ==========================================================
# Direct Excel Export
# ==========================================================

@import_export_bp.route(
    "/export/excel"
)
@login_required
def export_excel():

    filepath = CSVService.export_medicines_excel(
        current_user.id,
        "all"
    )

    return send_file(
        filepath,
        as_attachment=True
    )


# ==========================================================
# Download Sample CSV
# ==========================================================

@import_export_bp.route(
    "/sample"
)
@login_required
def download_sample():

    sample = os.path.join(
        "sample_data",
        "medicines.csv"
    )

    if not os.path.exists(sample):

        flash(
            "Sample CSV file not found.",
            "danger"
        )

        return redirect(
            url_for(
                "import_export.import_csv"
            )
        )

    return send_file(
        sample,
        as_attachment=True,
        download_name="medicines_sample.csv"
    )