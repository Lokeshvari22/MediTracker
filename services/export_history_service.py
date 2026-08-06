from database.database import db
from models.export_history import ExportHistory


class ExportHistoryService:

    @staticmethod
    def log_export(user_id, report_type, file_type, file_name=None):
        entry = ExportHistory(
            user_id=user_id,
            report_type=report_type,
            file_type=file_type,
            file_name=file_name
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def recent_exports(user_id, limit=10):
        return ExportHistory.query.filter_by(
            user_id=user_id
        ).order_by(
            ExportHistory.created_at.desc()
        ).limit(limit).all()
