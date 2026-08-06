"""
Import Validation Tests
Project: MediTracker

Purpose:
    Verify that all core MediTracker modules, database models,
    blueprints, and Flask application factories can be imported successfully.

Run:
    pytest tests/test_import.py
"""

import pytest


def test_core_imports():
    """Basic import checks for the current project layout."""
    try:
        from app import create_app
        from database.database import db
        # import a few models
        from models.user import User
        from models.medicine import Medicine
        from routes.report import report_bp

        assert create_app is not None
        assert db is not None
        assert User is not None
        assert Medicine is not None
        assert report_bp is not None

    except Exception as e:
        pytest.fail(f"Import failed: {e}")