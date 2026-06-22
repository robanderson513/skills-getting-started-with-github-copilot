import pytest


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success(client):
    email = "testuser@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]


def test_signup_duplicate(client):
    email = "emma@mergington.edu"
    response = client.post("/activities/Programming%20Class/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "new@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_participant_success(client):
    email = "testdelete@mergington.edu"
    client.post("/activities/Chess%20Club/signup", params={"email": email})

    response = client.delete(f"/activities/Chess%20Club/signup/{email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    response = client.get("/activities")
    assert email not in response.json()["Chess Club"]["participants"]


def test_delete_participant_not_registered(client):
    response = client.delete("/activities/Chess%20Club/signup/notregistered@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"


def test_delete_participant_nonexistent_activity(client):
    response = client.delete("/activities/Unknown%20Club/signup/test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
