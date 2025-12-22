import allure
from helpers.user_generator import UserGenerator
from helpers.api_client import ApiClient
from data.error_messages import AssertMessages, Error


class TestUserRegistration:

    @allure.epic("User API")
    @allure.feature("Создание пользователя")
    @allure.title("Создание пользователя")
    def test_registration(self):
        with allure.step("Подготовить тестовые данные"):
            payload = UserGenerator.generate_user_data()

        with allure.step("Отправить запрос на создание пользователя"):
            response = ApiClient.post_request_create_user(payload)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 201, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=201, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить тело ответа"):
            try:
                response_data = response.json()
            except ValueError:
                assert False, f"Response is not JSON: {response.text}"

            assert "user" in response_data, AssertMessages.FIELD_MISSING.format(
                field_name="user"
            )
            assert "id" in response_data["user"], AssertMessages.FIELD_MISSING.format(
                field_name="id"
            )
            assert "access_token" in response_data, AssertMessages.FIELD_MISSING.format(
                field_name="access_token"
            )
            # Исправлено: было 'access_token' in response_data['access_token'] — это ошибка

    @allure.title("Создание пользователя - пользователь уже существует")
    @allure.description(
        "Тест проверяет обработку ошибки при попытке создания пользователя с уже существующим email"
    )
    def test_existed_user_registration(self, register_and_login_user):
        with allure.step("Подготовить тестовые данные"):
            payload, _ = register_and_login_user

        with allure.step(
            "Отправить запрос на создание пользователя с существующим email"
        ):
            response = ApiClient.post_request_create_user(payload)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 400, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=400, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить сообщение об ошибке в ответе"):
            try:
                response_data = response.json()
            except ValueError:
                assert False, f"Response is not JSON: {response.text}"

            actual_message = response_data.get("message", "")
            assert (
                actual_message == Error.EMAIL_ALREADY_USED
            ), AssertMessages.ERROR_MESSAGE_MISMATCH.format(
                expected=ErrorMessages.EMAIL_ALREADY_IN_USE, actual=actual_message
            )
