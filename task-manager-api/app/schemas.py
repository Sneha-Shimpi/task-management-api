from datetime import date

from marshmallow import EXCLUDE, Schema, fields, validate

from app.models import VALID_PRIORITIES, VALID_SORT_FIELDS, VALID_SORT_ORDERS, VALID_STATUSES


class TaskCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(load_default="", validate=validate.Length(max=5000))
    status = fields.String(load_default="todo", validate=validate.OneOf(VALID_STATUSES))
    priority = fields.String(load_default="medium", validate=validate.OneOf(VALID_PRIORITIES))
    due_date = fields.Date(load_default=None, allow_none=True)


class TaskUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    status = fields.String(validate=validate.OneOf(VALID_STATUSES))
    priority = fields.String(validate=validate.OneOf(VALID_PRIORITIES))
    due_date = fields.Date(allow_none=True)


class TaskQuerySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status = fields.String(validate=validate.OneOf(VALID_STATUSES))
    priority = fields.String(validate=validate.OneOf(VALID_PRIORITIES))
    search = fields.String(load_default="")
    due_date = fields.Date(load_default=None, allow_none=True)
    sort_by = fields.String(load_default="created_at", validate=validate.OneOf(VALID_SORT_FIELDS))
    order = fields.String(load_default="desc", validate=validate.OneOf(VALID_SORT_ORDERS))
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=20, validate=validate.Range(min=1, max=100))


task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()
task_query_schema = TaskQuerySchema()
