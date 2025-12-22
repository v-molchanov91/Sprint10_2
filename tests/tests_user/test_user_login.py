import allure
from helpers.api_client import ApiClient
from data.error_messages import AssertMessages


@allure.suite("Авторизация")
class TestUserLogin:

    @allure.epic("User API")
    @allure.feature("Авторизация пользователя")
    @allure.title("Успешная авторизация пользователя")
    def test_user_login(self, register_new_user):
        with allure.step("Отправить запрос на авторизацию пользователя"):
            payload, _ = register_new_user
            response = ApiClient.post_request_login_user(payload)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 201, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=201, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить наличие access_token в ответе"):
            response_data = response.json()
            assert "token" in response_data, AssertMessages.FIELD_MISSING.format(
                field_name="token"
            )
            assert (
                "access_token" in response_data["token"]
            ), AssertMessages.FIELD_MISSING.format(field_name="access_token")
