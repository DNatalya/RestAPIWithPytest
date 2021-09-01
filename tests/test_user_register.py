import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.requests_helper import RequestsHelper


@allure.epic("User creation cases")
class TestUserRegister(BaseCase):
    @allure.description("Test for checking create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        response = RequestsHelper.post(url="/user/", data=self.prepare_registration_data(email))

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("Test for sucessfully user creation")
    def test_create_user_successfully(self):
        response = RequestsHelper.post(url="/user/", data=self.prepare_registration_data())

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

