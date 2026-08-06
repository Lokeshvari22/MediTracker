from database.database import db


class ExportHistory(db.Model):
    __tablename__ = "export_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    report_type = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        back_populates="exports"
    )
