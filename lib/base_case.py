import string, random
import json.decoder
import json
from datetime import datetime

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with name {header_name} in the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in Json format. Response text is {Response.text} "

        assert name in response_as_dict, f"Response JSON doesn't have {name}"
        return response_as_dict[name]

    def get_random_string(self, count_symbols=10):
        alphabet = string.ascii_lowercase + string.digits
        return ''.join([random.choice(alphabet) for i in range(count_symbols)])

    def prepare_registration_data(self, email=None, password=None, username=None, firstName=None, lastName=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        if password is None:
            password = self.get_random_string(4)
        if username is None:
            username = self.get_random_string(6)
        if firstName is None:
            firstName = self.get_random_string(8)
        if lastName is None:
            lastName = self.get_random_string(10)
        return {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'email': email}

