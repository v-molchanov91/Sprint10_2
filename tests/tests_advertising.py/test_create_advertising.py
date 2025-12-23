import allure
from helpers.listing_generator import ListingGenerator
from helpers.api_client import ApiClient
from data.error_messages import AssertMessages


class TestCreateAdvertising:

    @allure.feature("Создание объявления")
    @allure.title("Создание объявления")
    @allure.description("Тест проверяет успешное создание нового объявления")
    def test_create_listing(self, register_and_login_user):
        with allure.step("Подготовить тестовые данные"):
            _, headers = register_and_login_user
            payload = ListingGenerator.generate_listing_data()

        with allure.step("Отправить запрос на создание объявления"):
            response = ApiClient.post_request_create_listing(headers, payload)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 201, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=201, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить тело ответа"):
            response_data = response.json()
            assert "id" in response_data, AssertMessages.FIELD_MISSING.format(
                field_name="id"
            )
            assert "name" in response_data, AssertMessages.FIELD_MISSING.format(
                field_name="name"
            )
            assert (
                response_data["name"] == payload["name"]
            ), AssertMessages.FIELD_VALUE_MISMATCH.format(
                field_name="name",
                expected=payload["name"],
                actual=response_data.get("name"),
            )
