import pytest

from app import app, reset_tickets


@pytest.fixture
def client():
    reset_tickets()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_returns_200(client):
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_ticket_1_has_a_title(client):
    response = client.get("/api/tickets/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Laptop not charging"


def test_unknown_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404

def test_list_is_sorted_high_medium_low(client):
    response = client.get("/api/tickets")
    priorities = [t["priority"] for t in response.get_json()]
    assert priorities == ["High", "High", "Medium", "Medium", "Low"]

def test_empty_title_returns_400(client):
    response = client.post("/api/tickets", json={"title": "", "category": "Hardware", "priority": "High"})
    assert response.status_code == 400

def test_screen_shows_resolved_status(client):
    html = client.get("/").get_data(as_text=True)
    assert '<span class="badge">Resolved</span>' in html
# Add your own tests below: one failing test for each bug you find,

def test_unknown_category_returns_400(client):
    response = client.post("/api/tickets", json={"title": "Printer jam", "category": "Furniture"})
    assert response.status_code == 400


def test_unknown_priority_returns_400(client):
    response = client.post("/api/tickets", json={"title": "Printer jam", "priority": "Urgent"})
    assert response.status_code == 400


def test_blank_spaces_title_returns_400(client):
    response = client.post("/api/tickets", json={"title": "   "})
    assert response.status_code == 400


def test_missing_body_returns_400(client):
    response = client.post("/api/tickets")
    assert response.status_code == 400


def test_unknown_status_returns_400(client):
    response = client.patch("/api/tickets/1/status", json={"status": "Done"})
    assert response.status_code == 400


def test_status_change_on_missing_ticket_returns_404(client):
    response = client.patch("/api/tickets/9999/status", json={"status": "Closed"})
    assert response.status_code == 404
# plus at least 5 negative tests.
