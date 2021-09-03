import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.requests_helper import RequestsHelper


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):

    def setup(self):
        register_data = self.prepare_registration_data()
        response = RequestsHelper.post(url="/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data["email"]
        password = register_data["password"]
        self.user_id = self.get_json_value(response, "id")

        login_data = {
            "email": email,
            "password": password
        }

        response1 = RequestsHelper.post("/user/login", data=login_data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

    @allure.description("Test for failed delete user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature('Delete user', 'auth')
    def test_fail_delete_user(self):
        data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }

        response1 = RequestsHelper.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response = RequestsHelper.delete(url="/user/2",
                                         headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("Test for successful delete user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature('Delete user', 'auth')
    def test_successful_delete_user(self):
        response2 = RequestsHelper.delete(url=f"/user/{self.user_id}",
                                          headers={"x-csrf-token": self.token}, cookies={"auth_sid": self.auth_sid})
        Assertions.assert_code_status(response2, 200)

        response3 = RequestsHelper.get(f"/user/{self.user_id}")
        Assertions.assert_code_status(response3, 404)
        Assertions.assert_response_content(response3, "User not found")

    @allure.description("Test for failed delete user auth as other user")
    @allure.severity(allure.severity_level.MINOR)
    @allure.feature('Create user', 'Delete user', 'auth')
    def test_fail_delete_user_auth_as_other_user(self):
        register_data1 = self.prepare_registration_data()
        response2 = RequestsHelper.post(url="/user/", data=register_data1)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        user_id1 = self.get_json_value(response2, "id")

        response3 = RequestsHelper.delete(url=f"/user/{user_id1}",
                                          headers={"x-csrf-token": self.token}, cookies={"auth_sid": self.auth_sid})

        Assertions.assert_code_status(response3, 400)

