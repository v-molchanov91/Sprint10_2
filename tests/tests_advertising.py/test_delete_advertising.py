import allure
from helpers.api_client import ApiClient
from data.error_messages import AssertMessages
from data.response_messages import SuccessMessages


class TestDeleteAdvertsing:

    @allure.feature("Удаление объявления")
    @allure.title("Удаление объявления")
    @allure.description("Тест проверяет успешное удаление объявления")
    def test_delete_listing(self, created_listing):
        headers = created_listing["owner_headers"]
        listing_id = created_listing["listing_id"]

        with allure.step(f"Отправить запрос на удаление объявления ID={listing_id}"):
            response = ApiClient.delete_request_delete_listing(headers, listing_id)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=200, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить, что ответ — валидный JSON"):
            response_data = response.json()

        with allure.step("Проверить сообщение об успешном удалении"):
            assert "message" in response_data, AssertMessages.FIELD_MISSING.format(
                field_name="message"
            )
            actual_message = response_data["message"]
            assert (
                actual_message == SuccessMessages.DELETED_SUCCESS
            ), AssertMessages.FIELD_VALUE_MISMATCH.format(
                field_name="message",
                expected=SuccessMessages.DELETED_SUCCESS,
                actual=actual_message,
            )
