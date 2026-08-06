from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip()

        password = request.form.get("password", "")

        user = AuthService.authenticate_user(
            email,
            password
        )

        if user:

            login_user(user)

            flash(
                "Login Successful!",
                "success"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

        flash(
            "Invalid Email or Password.",
            "danger"
        )

    return render_template("login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        email = request.form.get(
            "email",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template(
                "signup.html"
            )

        success, message = AuthService.register_user(
            username,
            email,
            password
        )

        if success:

            flash(
                message,
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

        flash(
            message,
            "danger"
        )

    return render_template(
        "signup.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )