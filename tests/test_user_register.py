import allure
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.requests_helper import RequestsHelper


@allure.epic("User creation cases")
class TestUserRegister(BaseCase):

    @allure.description("Test for checking create user with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature('Create user')
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        response = RequestsHelper.post(url="/user/", data=self.prepare_registration_data(email))

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"Users with email '{email}' already exists")

    @allure.description("Test for sucessfully user creation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature('Create user')
    def test_create_user_successfully(self):
        response = RequestsHelper.post(url="/user/", data=self.prepare_registration_data())

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("Test for user creation with invalid email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature('Create user')
    def test_create_user_with_invalid_email(self):
        email = "noname.ya.ru"
        response = RequestsHelper.post(url="/user/", data=self.prepare_registration_data(email))

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    data_params = [
        ("email", None, "learnqa", "123","learnqa", "learnqa"),
        ("username", "test@example.ru", None, "123","learnqa", "learnqa"),
        ("password", "test@example.ru", "learnqa", None,"learnqa", "learnqa"),
        ("firstName", "test@example.ru", "learnqa", "123", None, "learnqa"),
        ("lastName", "test@example.ru", "learnqa", "123",  "learnqa", None)
    ]

    @allure.description("Check for user creation without any param")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature('Create user')
    @pytest.mark.parametrize('name, email, username, password, firstName, lastName', data_params)
    def test_create_user_without_param(self, name, email, username, password, firstName, lastName):
        response = RequestsHelper.post(url="/user/",
                                       data={"email": email,
                                             "username": username,
                                             "password": password,
                                             "firstName": firstName,
                                             "lastName": lastName
                                             })

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"The following required params are missed: {name}")

    @allure.description("Test for user creation with short name")
    @allure.severity(allure.severity_level.MINOR)
    @allure.feature('Create user')
    def test_create_user_with_short_name(self):
        response = RequestsHelper.post(url="/user/", data=self.prepare_registration_data(firstName=
                                                                                         self.get_random_string(1)))
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "The value of 'firstName' field is too short")

    @allure.description("Test for user creation with long name")
    @allure.severity(allure.severity_level.MINOR)
    @allure.feature('Create user')
    def test_create_user_with_long_name(self):
        response = RequestsHelper.post(url="/user/", data=self.prepare_registration_data(firstName=
                                                                                         self.get_random_string(251)))
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "The value of 'firstName' field is too long")
