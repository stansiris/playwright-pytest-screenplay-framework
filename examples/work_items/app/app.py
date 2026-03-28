"""Work Items Flask application routes and web/API entrypoints."""

from __future__ import annotations

import os
from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from . import db, seed

FILTER_TO_STATUS = {
    "all": None,
    "active": "ACTIVE",
    "completed": "COMPLETED",
}


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_mapping(
        SECRET_KEY=os.getenv("WORK_ITEMS_SECRET_KEY", "work-items-dev-secret"),
        WORK_ITEMS_DB_PATH=str(db.get_db_path()),
    )

    if test_config:
        app.config.update(test_config)

    db_path = _db_path_from_app(app)
    db.init_database(db_path)
    seed.seed_default_user(db_path=db_path)
    seed.seed_secondary_user(db_path=db_path)

    def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(view)
        def wrapped(*args: Any, **kwargs: Any):
            if not _current_user():
                return redirect(url_for("login"))
            return view(*args, **kwargs)

        return wrapped

    def api_login_required(view: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(view)
        def wrapped(*args: Any, **kwargs: Any):
            if not _current_user():
                return _json_error("Unauthorized.", 401)
            return view(*args, **kwargs)

        return wrapped

    def _create_ui_work_item() -> tuple[str, int]:
        username = _current_user()
        if username is None:
            return "Not authenticated.", 401

        title = request.form.get("title", "")
        description = request.form.get("description")
        priority = request.form.get("priority", "MEDIUM")
        due_date = request.form.get("due_date")

        try:
            db.create_work_item(
                owner_username=username,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                db_path=db_path,
            )
        except ValueError as exc:
            return str(exc), 400

        return "Work item created successfully.", 201

    @app.get("/")
    def home():
        if _current_user():
            return redirect(url_for("work_items_dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error_message = ""
        entered_username = ""
        if request.method == "POST":
            entered_username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not entered_username or not password:
                error_message = "Username and password are required."
            else:
                user = db.get_user(entered_username, db_path=db_path)
                if user and check_password_hash(user["password_hash"], password):
                    session["username"] = entered_username
                    flash("Login successful.", "success")
                    return redirect(url_for("work_items_dashboard"))
                error_message = "Invalid username or password."

        return render_template(
            "login.html",
            error_message=error_message,
            entered_username=entered_username,
        )

    @app.post("/logout")
    def logout():
        session.clear()
        flash("Logged out.", "success")
        return redirect(url_for("login"))

    @app.get("/work-items")
    @login_required
    def work_items_dashboard():
        active_filter = _normalize_filter(request.args.get("filter"))
        edit_work_item_id = _safe_int(request.args.get("edit"))
        work_items = db.list_work_items(
            owner_username=_current_user() or "",
            status_filter=active_filter,
            db_path=db_path,
        )
        return render_template(
            "work_items.html",
            work_items=work_items,
            active_filter=active_filter,
            edit_work_item_id=edit_work_item_id,
        )

    @app.post("/work-items/create")
    @login_required
    def create_work_item_ui():
        current_filter = _normalize_filter(request.form.get("current_filter"))
        message, status_code = _create_ui_work_item()
        flash(message, "success" if status_code == 201 else "error")
        return redirect(url_for("work_items_dashboard", filter=current_filter))

    @app.post("/work-items/<int:work_item_id>/edit")
    @login_required
    def edit_work_item_ui(work_item_id: int):
        current_filter = _normalize_filter(request.form.get("current_filter"))
        username = _current_user() or ""

        if db.get_work_item_by_id(work_item_id, username, db_path=db_path) is None:
            flash("Work item not found.", "error")
            return redirect(url_for("work_items_dashboard", filter=current_filter))

        try:
            db.update_work_item(
                work_item_id=work_item_id,
                owner_username=username,
                title=request.form.get("title"),
                description=request.form.get("description"),
                priority=request.form.get("priority"),
                due_date=request.form.get("due_date"),
                db_path=db_path,
            )
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(
                url_for("work_items_dashboard", filter=current_filter, edit=work_item_id)
            )

        flash("Work item updated successfully.", "success")
        return redirect(url_for("work_items_dashboard", filter=current_filter))

    @app.post("/work-items/<int:work_item_id>/toggle")
    @login_required
    def toggle_work_item_ui(work_item_id: int):
        current_filter = _normalize_filter(request.form.get("current_filter"))
        username = _current_user() or ""
        work_item = db.get_work_item_by_id(work_item_id, username, db_path=db_path)
        if work_item is None:
            flash("Work item not found.", "error")
            return redirect(url_for("work_items_dashboard", filter=current_filter))

        next_status = "COMPLETED" if work_item["status"] == "ACTIVE" else "ACTIVE"
        db.update_work_item(
            work_item_id=work_item_id,
            owner_username=username,
            status=next_status,
            db_path=db_path,
        )
        flash(
            (
                "Work item marked completed."
                if next_status == "COMPLETED"
                else "Work item marked active."
            ),
            "success",
        )
        return redirect(url_for("work_items_dashboard", filter=current_filter))

    @app.post("/work-items/<int:work_item_id>/delete")
    @login_required
    def delete_work_item_ui(work_item_id: int):
        current_filter = _normalize_filter(request.form.get("current_filter"))
        username = _current_user() or ""
        deleted = db.delete_work_item(work_item_id, username, db_path=db_path)
        if deleted:
            flash("Work item deleted successfully.", "success")
        else:
            flash("Work item not found.", "error")
        return redirect(url_for("work_items_dashboard", filter=current_filter))

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/api/login")
    def api_login():
        payload = request.get_json(silent=True) or {}
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        if not username or not password:
            return _json_error("Username and password are required.", 400)

        user = db.get_user(username, db_path=db_path)
        if user is None or not check_password_hash(user["password_hash"], password):
            return _json_error("Invalid credentials.", 401)

        session["username"] = username
        return jsonify({"username": username})

    @app.post("/api/logout")
    def api_logout():
        session.clear()
        return jsonify({"message": "Logged out."})

    @app.get("/api/me")
    @api_login_required
    def api_me():
        return jsonify({"username": _current_user()})

    @app.route("/api/work-items", methods=["GET", "POST"])
    @api_login_required
    def api_work_items():
        username = _current_user() or ""
        if request.method == "GET":
            active_filter = _normalize_filter(request.args.get("filter"))
            work_items = db.list_work_items(
                owner_username=username,
                status_filter=active_filter,
                db_path=db_path,
            )
            return jsonify({"work_items": work_items})

        payload = request.get_json(silent=True) or {}
        title = payload.get("title", "")
        description = payload.get("description")
        priority = payload.get("priority", "MEDIUM")
        due_date = payload.get("due_date")
        status = payload.get("status", "ACTIVE")

        try:
            work_item = db.create_work_item(
                owner_username=username,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                status=status,
                db_path=db_path,
            )
        except ValueError as exc:
            return _json_error(str(exc), 400)

        return jsonify(work_item), 201

    @app.route("/api/work-items/<int:work_item_id>", methods=["GET", "PUT", "DELETE"])
    @api_login_required
    def api_work_item_by_id(work_item_id: int):
        username = _current_user() or ""
        owner = db.get_work_item_owner(work_item_id, db_path=db_path)
        if owner is None:
            return _json_error("Work item not found.", 404)
        if owner != username:
            return _json_error("Access forbidden.", 403)

        if request.method == "GET":
            existing = db.get_work_item_by_id(work_item_id, username, db_path=db_path)
            return jsonify(existing)

        if request.method == "DELETE":
            db.delete_work_item(work_item_id, username, db_path=db_path)
            return "", 204

        payload = request.get_json(silent=True) or {}
        update_kwargs: dict[str, Any] = {}
        for field in ("title", "description", "status", "priority", "due_date"):
            if field in payload:
                update_kwargs[field] = payload[field]

        if not update_kwargs:
            return _json_error("No updatable fields provided.", 400)

        try:
            updated = db.update_work_item(
                work_item_id=work_item_id,
                owner_username=username,
                db_path=db_path,
                **update_kwargs,
            )
        except ValueError as exc:
            return _json_error(str(exc), 400)

        if updated is None:
            return _json_error("Work item not found.", 404)
        return jsonify(updated)

    @app.post("/api/test/reset")
    def api_test_reset():
        session.clear()
        seed_result = seed.reset_and_seed(db_path=db_path)
        return jsonify(
            {
                "message": "Reset complete.",
                "seed": seed_result,
            }
        )

    @app.post("/api/test/seed")
    def api_test_seed():
        seed.seed_default_user(db_path=db_path)
        seed.seed_secondary_user(db_path=db_path)
        work_items = seed.seed_default_work_items(db_path=db_path, replace_existing=True)
        return jsonify(
            {
                "message": "Seed complete.",
                "username": seed.DEFAULT_USERNAME,
                "work_item_count": len(work_items),
            }
        )

    return app


def _db_path_from_app(app: Flask) -> str:
    return str(app.config["WORK_ITEMS_DB_PATH"])


def _current_user() -> str | None:
    username = session.get("username")
    if isinstance(username, str) and username.strip():
        return username
    return None


def _normalize_filter(raw_filter: str | None) -> str:
    normalized = (raw_filter or "all").strip().lower()
    if normalized not in FILTER_TO_STATUS:
        return "all"
    return normalized


def _safe_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _json_error(message: str, status_code: int):
    return jsonify({"error": message}), status_code


if __name__ == "__main__":
    run_port = int(os.getenv("WORK_ITEMS_PORT", "5001"))
    create_app().run(host="127.0.0.1", port=run_port, debug=False, use_reloader=False)
