import pytest
import sys
import os
from helpers.user_generator import UserGenerator
from helpers.listing_generator import ListingGenerator
from helpers.api_client import ApiClient


@pytest.fixture
def register_new_user():
    payload = UserGenerator.generate_user_data()
    response = ApiClient.post_request_create_user(payload)

    if response.status_code != 201:
        pytest.fail(f"Failed to register user: {response.status_code}, {response.text}")

    try:
        response_data = response.json()
        auth_token = response_data["access_token"]["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        return payload, headers
    except (KeyError, ValueError) as e:
        pytest.fail(f"Invalid response format during user registration: {e}")


@pytest.fixture(scope="session")
def register_and_login_user():
    payload = UserGenerator.generate_user_data()

    reg_response = ApiClient.post_request_create_user(payload)
    if reg_response.status_code != 201:
        pytest.fail(
            f"Failed to register user: {reg_response.status_code}, {reg_response.text}"
        )

    try:
        token = reg_response.json()["access_token"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    except (KeyError, ValueError):
        pytest.fail("Registration response missing access_token")

    # Опционально: делаем запрос на login (если API требует отдельного входа)
    # Если login не нужен (токен уже есть), можно пропустить
    login_response = ApiClient.post_request_login_user(payload)
    if login_response.status_code != 201:
        # Раскомментируй, если login обязателен. Иначе — игнорируем.
        # pytest.fail(f"Failed to login user: {login_response.status_code}, {login_response.text}")
        pass  # или оставить как есть, если токен из /register валиден

    return payload, headers


@pytest.fixture
def created_listing(register_and_login_user):
    _, headers = register_and_login_user
    payload = ListingGenerator.generate_listing_data()

    response = ApiClient.post_request_create_listing(headers, data=payload)

    if response.status_code != 201:
        pytest.fail(
            f"Failed to create listing: {response.status_code}, {response.text}"
        )

    try:
        json_data = response.json()
        return {
            "listing_id": json_data["id"],
            "original_price": json_data["price"],
            "owner_headers": headers,
            "original_payload": payload,
        }
    except (KeyError, ValueError) as e:
        pytest.fail(f"Invalid listing response format: {e}")
