import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.requests_helper import RequestsHelper


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):

    def setup(self):
        register_data = self.prepare_registration_data()
        response = RequestsHelper.post(url="/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data["email"]
        password = register_data["password"]
        self.user_id = self.get_json_value(response, "id")

        self.login_data = {
            "email": email,
            "password": password
        }

        response1 = RequestsHelper.post("/user/login", data=self.login_data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

    @allure.description("Test for edit first name for just created user")
    def test_edit_just_created_user(self):
        new_name = "changed_name"
        response2 = RequestsHelper.put(f"/user/{self.user_id}",
                                       headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid},
                                       data={"firstName": new_name})

        Assertions.assert_code_status(response2, 200)

        response3 = RequestsHelper.get(f"/user/{self.user_id}",
                                       headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response3, "firstName", new_name, "Wrong name of user after edit")

    @allure.description("Test for edit first name user without auth")
    def test_edit_user_without_auth(self):
        new_name = "Olga"
        response2 = RequestsHelper.put(f"/user/{self.user_id}",
                                       data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_content(response2, "Auth token not supplied")

    @allure.description("Test for edit last name user with auth as other user")
    def test_edit_user_with_auth_as_other_user(self):
        last_name = "Boyko"

        register_data1 = self.prepare_registration_data()
        response2 = RequestsHelper.post(url="/user/", data=register_data1)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        user_id1 = self.get_json_value(response2, "id")

        response3 = RequestsHelper.put(f"/user/{user_id1}",
                                       data={"lastName": last_name},
                                       headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid})

        Assertions.assert_code_status(response3, 400)

    @allure.description("Test for check edit user with invalid email")
    def test_edit_user_with_invalid_email(self):
        new_email = "noname.ya.ru"

        response2 = RequestsHelper.put(f"/user/{self.user_id}",
                                       data={"email": new_email},
                                       headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_content(response2, "Invalid email format")

    @allure.description("Test for check edit user with short first name")
    def test_edit_user_with_short_first_name(self):
        response2 = RequestsHelper.put(f"/user/{self.user_id}",
                                       data={"firstName": self.get_random_string(1)},
                                       headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(response2, "error", "Too short value for field firstName",
                                             f"Unexpected response content {response2.text}")
