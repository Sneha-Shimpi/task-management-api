from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import or_

from app.extensions import db
from app.models import Task
from app.schemas import task_create_schema, task_query_schema, task_update_schema

api = Blueprint("api", __name__, url_prefix="/api")


def error_response(message, status_code, details=None):
    payload = {"error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status_code


@api.errorhandler(ValidationError)
def handle_validation_error(err):
    return error_response("Validation failed", 400, err.messages)


@api.route("/tasks", methods=["POST"])
def create_task():
    data = task_create_schema.load(request.get_json(silent=True) or {})
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api.route("/tasks", methods=["GET"])
def list_tasks():
    params = task_query_schema.load(request.args)
    query = Task.query

    if "status" in params:
        query = query.filter_by(status=params["status"])
    if "priority" in params:
        query = query.filter_by(priority=params["priority"])
    if params.get("due_date"):
        query = query.filter(Task.due_date == params["due_date"])
    if params.get("search"):
        search_term = f"%{params['search']}%"
        query = query.filter(or_(Task.title.ilike(search_term), Task.description.ilike(search_term)))

    sort_field = params.get("sort_by", "created_at")
    sort_order = params.get("order", "desc")
    sort_column = getattr(Task, sort_field)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    pagination = query.paginate(
        page=params["page"], per_page=params["per_page"], error_out=False
    )

    total_tasks = pagination.total
    done_count = Task.query.filter_by(status="done").count()
    todo_count = Task.query.filter_by(status="todo").count()
    in_progress_count = Task.query.filter_by(status="in_progress").count()
    high_priority_count = Task.query.filter_by(priority="high").count()
    completion_rate = round((done_count / total_tasks * 100) if total_tasks else 0)

    return jsonify(
        {
            "tasks": [t.to_dict() for t in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": total_tasks,
            "total_pages": pagination.pages,
            "summary": {
                "total": total_tasks,
                "todo": todo_count,
                "in_progress": in_progress_count,
                "done": done_count,
                "high_priority": high_priority_count,
                "completion_rate": completion_rate,
            },
        }
    )


@api.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return error_response(f"Task {task_id} not found", 404)
    return jsonify(task.to_dict())


@api.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return error_response(f"Task {task_id} not found", 404)

    data = task_update_schema.load(request.get_json(silent=True) or {})
    if not data:
        return error_response("No valid fields provided to update", 400)

    for key, value in data.items():
        setattr(task, key, value)

    db.session.commit()
    return jsonify(task.to_dict())


@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return error_response(f"Task {task_id} not found", 404)

    db.session.delete(task)
    db.session.commit()
    return "", 204


@api.route("/openapi.json", methods=["GET"])
def openapi_spec():
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "TaskFlow API",
            "version": "1.0.0",
            "description": "Modern task management API with CRUD, filtering, search, sorting, and pagination.",
        },
        "paths": {
            "/api/tasks": {
                "get": {"summary": "List tasks"},
                "post": {"summary": "Create task"},
            },
            "/api/tasks/{task_id}": {
                "get": {"summary": "Get a task"},
                "put": {"summary": "Update a task"},
                "delete": {"summary": "Delete a task"},
            },
        },
    }
    return jsonify(spec)
