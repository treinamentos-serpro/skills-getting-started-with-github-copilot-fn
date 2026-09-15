def test_get_activities_returns_all_activity_details(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == 9
    assert expected_activity in activities
    assert set(activities[expected_activity]) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "student@example.com"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_removes_student_from_activity(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "student@example.com"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_activity_state_is_reset_between_tests(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "student@example.com"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert email not in response.json()[activity_name]["participants"]
