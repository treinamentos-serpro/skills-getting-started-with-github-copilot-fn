import pytest


@pytest.mark.parametrize(
    "method, activity_name, email, expected_detail",
    [
        (
            "post",
            "Unknown Club",
            "student@example.com",
            "Activity not found",
        ),
        (
            "delete",
            "Unknown Club",
            "student@example.com",
            "Activity not found",
        ),
    ],
)
def test_unknown_activity_returns_not_found(
    client, method, activity_name, email, expected_detail
):
    # Arrange
    request = getattr(client, method)

    # Act
    response = request(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == expected_detail


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "student@example.com"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregistering_unknown_student_returns_not_found(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "student@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


@pytest.mark.parametrize("method", ["post", "delete"])
def test_signup_requires_email(client, method):
    # Arrange
    request = getattr(client, method)

    # Act
    response = request("/activities/Soccer Club/signup")

    # Assert
    assert response.status_code == 422
