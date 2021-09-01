import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.requests_helper import RequestsHelper


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    @allure.description("Test for edit first name for just created user")
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response = RequestsHelper.post(url="/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response, "id")

        login_data = {
            "email": email,
            "password": password
        }

        response1 = RequestsHelper.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        new_name = "changed_name"
        response2 = RequestsHelper.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response2, 200)

        response3 = RequestsHelper.get(f"/user/{user_id}",
                                              headers={"x-csrf-token": token},
                                              cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response3, "firstName", new_name, "Wrong name of user after edit")