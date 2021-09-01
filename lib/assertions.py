import json

from requests import Response


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in Json format. Response text is {Response.text} "

        assert name in response_as_dict, f"Response JSON doesn't have {name}"
        assert response_as_dict[name] == expected_value, error

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in Json format. Response text is {Response.text} "

        assert name in response_as_dict, f"Response JSON doesn't have {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in Json format. Response text is {Response.text} "

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have {name}"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in Json format. Response text is {Response.text} "

        assert name not in response_as_dict, f"Response JSON shouldn't have {name}, but it has present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code,\
            f"Unexpected status code. Expected {expected_status_code}, actual {response.status_code}"

    @staticmethod
    def assert_response_content(response: Response, expected_value):
        assert response.content.decode(
            "utf-8") == expected_value, f"Unexpected response content {response.content}"