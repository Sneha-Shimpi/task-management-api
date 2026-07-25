def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_index_page_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Task Log" in resp.data


class TestCreateTask:
    def test_create_task_success(self, client):
        resp = client.post(
            "/api/tasks",
            json={"title": "Buy milk", "description": "2%", "priority": "low"},
        )
        body = resp.get_json()
        assert resp.status_code == 201
        assert body["title"] == "Buy milk"
        assert body["status"] == "todo"  # default
        assert body["priority"] == "low"
        assert "id" in body and "created_at" in body

    def test_create_task_defaults(self, client):
        resp = client.post("/api/tasks", json={"title": "Minimal task"})
        body = resp.get_json()
        assert resp.status_code == 201
        assert body["status"] == "todo"
        assert body["priority"] == "medium"
        assert body["description"] == ""

    def test_create_task_missing_title_fails(self, client):
        resp = client.post("/api/tasks", json={"description": "no title"})
        assert resp.status_code == 400
        assert "title" in resp.get_json()["details"]

    def test_create_task_invalid_status_fails(self, client):
        resp = client.post(
            "/api/tasks", json={"title": "Bad status", "status": "not_a_status"}
        )
        assert resp.status_code == 400
        assert "status" in resp.get_json()["details"]

    def test_create_task_empty_title_fails(self, client):
        resp = client.post("/api/tasks", json={"title": ""})
        assert resp.status_code == 400

    def test_create_task_no_body_fails(self, client):
        resp = client.post("/api/tasks", data="", content_type="application/json")
        assert resp.status_code == 400


class TestGetTask:
    def test_get_task_success(self, client, sample_task):
        resp = client.get(f"/api/tasks/{sample_task['id']}")
        assert resp.status_code == 200
        assert resp.get_json()["id"] == sample_task["id"]

    def test_get_task_not_found(self, client):
        resp = client.get("/api/tasks/9999")
        assert resp.status_code == 404
        assert "error" in resp.get_json()


class TestListTasks:
    def test_list_empty(self, client):
        resp = client.get("/api/tasks")
        body = resp.get_json()
        assert resp.status_code == 200
        assert body["tasks"] == []
        assert body["total"] == 0

    def test_list_returns_created_tasks(self, client, sample_task):
        resp = client.get("/api/tasks")
        body = resp.get_json()
        assert body["total"] == 1
        assert body["tasks"][0]["id"] == sample_task["id"]

    def test_filter_by_status(self, client):
        client.post("/api/tasks", json={"title": "A", "status": "todo"})
        client.post("/api/tasks", json={"title": "B", "status": "done"})

        resp = client.get("/api/tasks?status=done")
        body = resp.get_json()
        assert body["total"] == 1
        assert body["tasks"][0]["title"] == "B"

    def test_filter_by_priority(self, client):
        client.post("/api/tasks", json={"title": "A", "priority": "low"})
        client.post("/api/tasks", json={"title": "B", "priority": "high"})

        resp = client.get("/api/tasks?priority=high")
        body = resp.get_json()
        assert body["total"] == 1
        assert body["tasks"][0]["title"] == "B"

    def test_filter_by_status_and_priority(self, client):
        client.post("/api/tasks", json={"title": "A", "status": "todo", "priority": "high"})
        client.post("/api/tasks", json={"title": "B", "status": "done", "priority": "high"})

        resp = client.get("/api/tasks?status=done&priority=high")
        body = resp.get_json()
        assert body["total"] == 1
        assert body["tasks"][0]["title"] == "B"

    def test_invalid_filter_value_fails(self, client):
        resp = client.get("/api/tasks?status=bogus")
        assert resp.status_code == 400

    def test_pagination(self, client):
        for i in range(5):
            client.post("/api/tasks", json={"title": f"Task {i}"})

        resp = client.get("/api/tasks?page=1&per_page=2")
        body = resp.get_json()
        assert len(body["tasks"]) == 2
        assert body["total"] == 5
        assert body["total_pages"] == 3


class TestUpdateTask:
    def test_update_task_success(self, client, sample_task):
        resp = client.put(
            f"/api/tasks/{sample_task['id']}", json={"status": "in_progress"}
        )
        body = resp.get_json()
        assert resp.status_code == 200
        assert body["status"] == "in_progress"
        assert body["title"] == sample_task["title"]  # unchanged

    def test_update_task_not_found(self, client):
        resp = client.put("/api/tasks/9999", json={"status": "done"})
        assert resp.status_code == 404

    def test_update_task_invalid_value_fails(self, client, sample_task):
        resp = client.put(
            f"/api/tasks/{sample_task['id']}", json={"priority": "urgent"}
        )
        assert resp.status_code == 400

    def test_update_task_empty_body_fails(self, client, sample_task):
        resp = client.put(f"/api/tasks/{sample_task['id']}", json={})
        assert resp.status_code == 400


class TestDeleteTask:
    def test_delete_task_success(self, client, sample_task):
        resp = client.delete(f"/api/tasks/{sample_task['id']}")
        assert resp.status_code == 204

        follow_up = client.get(f"/api/tasks/{sample_task['id']}")
        assert follow_up.status_code == 404

    def test_delete_task_not_found(self, client):
        resp = client.delete("/api/tasks/9999")
        assert resp.status_code == 404


def test_create_task_accepts_due_date(client):
    resp = client.post(
        "/api/tasks",
        json={"title": "Ship milestone", "due_date": "2026-08-20"},
    )
    body = resp.get_json()
    assert resp.status_code == 201
    assert body["due_date"] == "2026-08-20"


def test_list_tasks_supports_search_and_sort(client):
    client.post("/api/tasks", json={"title": "Alpha task", "priority": "high"})
    client.post("/api/tasks", json={"title": "Beta task", "priority": "low"})

    resp = client.get("/api/tasks?search=alpha&sort_by=priority&order=desc")
    body = resp.get_json()

    assert resp.status_code == 200
    assert body["tasks"][0]["title"] == "Alpha task"


def test_openapi_documentation_is_available(client):
    resp = client.get("/api/openapi.json")
    assert resp.status_code == 200
    assert resp.get_json()["info"]["title"] == "TaskFlow API"
