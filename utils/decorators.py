from functools import wraps

from flask import (
    request,
    jsonify,
    flash,
    redirect,
    url_for
)

from flask_login import current_user


# ==========================================================
# Admin Required
# ==========================================================

def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:

            flash(
                "Please login first.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        if getattr(
            current_user,
            "role",
            "User"
        ) != "Admin":

            flash(
                "Administrator access required.",
                "danger"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

        return function(
            *args,
            **kwargs
        )

    return wrapper


# ==========================================================
# AJAX Request Only
# ==========================================================

def ajax_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if request.headers.get(
            "X-Requested-With"
        ) != "XMLHttpRequest":

            return jsonify({

                "success": False,

                "message": "AJAX request required."

            }), 400

        return function(
            *args,
            **kwargs
        )

    return wrapper


# ==========================================================
# JSON Request Validation
# ==========================================================

def validate_json(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not request.is_json:

            return jsonify({

                "success": False,

                "message": "JSON request expected."

            }), 400

        return function(
            *args,
            **kwargs
        )

    return wrapper


# ==========================================================
# Standard API Response
# ==========================================================

def api_response(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        try:

            result = function(
                *args,
                **kwargs
            )

            return jsonify({

                "success": True,

                "data": result

            })

        except Exception as error:

            return jsonify({

                "success": False,

                "message": str(error)

            }), 500

    return wrapper


# ==========================================================
# Log Route Activity
# ==========================================================

def log_activity(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        user = (

            current_user.username

            if current_user.is_authenticated

            else "Anonymous"

        )

        print(

            f"[Activity] "

            f"{user} -> "

            f"{request.method} "

            f"{request.path}"

        )

        return function(
            *args,
            **kwargs
        )

    return wrapper


# ==========================================================
# Handle Database Exceptions
# ==========================================================

def handle_exceptions(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        try:

            return function(
                *args,
                **kwargs
            )

        except Exception as error:

            flash(
                str(error),
                "danger"
            )

            return redirect(
                request.referrer
                or url_for(
                    "dashboard.dashboard"
                )
            )

    return wrapper


# ==========================================================
# Cache Control
# ==========================================================

def no_cache(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        response = function(
            *args,
            **kwargs
        )

        response.headers[

            "Cache-Control"

        ] = (

            "no-store, "

            "no-cache, "

            "must-revalidate"

        )

        response.headers[

            "Pragma"

        ] = "no-cache"

        response.headers[

            "Expires"

        ] = "0"

        return response

    return wrapper