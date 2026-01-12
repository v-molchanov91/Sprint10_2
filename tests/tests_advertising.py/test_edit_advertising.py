import allure
from helpers.listing_generator import ListingGenerator
from helpers.api_client import ApiClient
from data.error_messages import AssertMessages
from data.response_messages import ErrorResponseMessages


class TestEditAdvertising:

    @allure.feature("Редактирование объявления")
    @allure.title("Редактирование объявления существующий пользователь")
    @allure.description("Тест проверяет успешное редактирование объявления владельцем")
    def test_edit_listing_by_owner(self, created_listing):
        with allure.step("Подготовить данные для обновления"):
            updated_payload = ListingGenerator.generate_listing_data(price="2895")

        with allure.step("Отправить запрос на редактирование объявления"):
            response = ApiClient.patch_request_update_listing(
                headers=created_listing["owner_headers"],
                listing_id=created_listing["listing_id"],
                data=updated_payload,
            )

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=200, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить, что ответ — валидный JSON"):
            try:
                response_data = response.json()
            except ValueError:
                assert False, f"Response is not JSON: {response.text}"

        with allure.step("Проверить, что цена изменилась"):
            original_price = created_listing["original_price"]
            new_price = response_data.get("price")
            assert new_price is not None, "Field 'price' is missing in response"
            assert (
                str(new_price) == updated_payload["price"]
            ), AssertMessages.FIELD_VALUE_MISMATCH.format(
                field_name="price", expected=updated_payload["price"], actual=new_price
            )
            assert str(new_price) != str(
                original_price
            ), f"Цена не изменилась: была {original_price}, стала {new_price}"

    @allure.feature("Редактирование объявления")
    @allure.title("Редактирование объявления не зарегестрированным пользователем")
    @allure.description("Тест проверяет ошибку при редактировании без токена")
    def test_edit_listing_unauthorized(self, created_listing):
        with allure.step("Подготовить данные для обновления"):
            updated_payload = ListingGenerator.generate_listing_data(price="3876")
            headers_unauthorized = {}

        with allure.step("Отправить запрос на редактирование без авторизации"):
            response = ApiClient.patch_request_update_listing(
                headers=headers_unauthorized,
                listing_id=created_listing["listing_id"],
                data=updated_payload,
            )

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 401, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=401, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить тело ответа"):
            try:
                response_data = response.json()
            except ValueError:
                assert False, f"Response is not JSON: {response.text}"

            actual_message = response_data.get("messege")
            assert (
                actual_message == ErrorResponseMessages.TOKEN_INVALID
            ), AssertMessages.FIELD_VALUE_MISMATCH.format(
                field_name="messege",
                expected=ErrorResponseMessages.TOKEN_INVALID,
                actual=actual_message,
            )

    @allure.feature("Редактирование объявления")
    @allure.title("Редактирование объявления чужого объявления")
    @allure.description("Тест проверяет ошибку при редактировании чужого объявления")
    def test_edit_listing_by_another_user(self, created_listing, register_new_user):
        with allure.step("Подготовить данные для обновления"):
            _, another_headers = register_new_user
            updated_payload = ListingGenerator.generate_listing_data(price="6735")

        with allure.step("Отправить запрос на редактирование чужого объявления"):
            response = ApiClient.patch_request_update_listing(
                headers=another_headers,
                listing_id=created_listing["listing_id"],
                data=updated_payload,
            )

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 401, (
                AssertMessages.STATUS_CODE_MISMATCH.format(
                    expected=401, actual=response.status_code
                )
                + f" Response: {response.text}"
            )

        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()

            actual_message = response_data.get("message")
            assert (
                actual_message == ErrorResponseMessages.LISTING_NOT_FOUND
            ), AssertMessages.FIELD_VALUE_MISMATCH.format(
                field_name="message",
                expected=ErrorResponseMessages.LISTING_NOT_FOUND,
                actual=actual_message,
            )
