import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.requests_helper import RequestsHelper


@allure.epic("Get user details cases")
class TestUserGet(BaseCase):

    def setup(self):
        data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }

        response1 = RequestsHelper.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("Test for get user details without auth")
    def test_get_user_details_not_auth(self):
        response = RequestsHelper.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    @allure.description("Test for get user details with auth")
    def test_get_user_details_auth_as_same_user(self):
        response = RequestsHelper.get(f"/user/{self.user_id_from_auth_method}",
                                      headers={"x-csrf-token": self.token}, cookies={"auth_sid": self.auth_sid})
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response, expected_fields)

    @allure.description("Test for get user details with auth as other user")
    def test_get_user_details_auth_as_other_user(self):
        response = RequestsHelper.get(f"/user/{int(self.user_id_from_auth_method)-1}",
                                      headers={"x-csrf-token": self.token}, cookies={"auth_sid": self.auth_sid})
        expected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_no_keys(response, expected_fields)
