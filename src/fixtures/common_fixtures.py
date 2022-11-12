from json import dumps, load, loads
from typing import Callable, List, Tuple, Union

import pytest


__all__: Tuple = ("json_data_by_path", "payload_and_response_data_by_path", "remove_uuid_fields_from_response")


@pytest.fixture
def json_data_by_path() -> Callable[[str], dict]:
    def func(file_path: str) -> dict:
        with open(file_path, mode="r") as file:
            json_data = load(file)
        return json_data

    return func


@pytest.fixture
def payload_and_response_data_by_path() -> Callable[[str], Tuple[dict, dict]]:
    def func(file_path: str) -> Tuple[dict, dict]:
        with open(file_path, mode="r") as file:
            json_data = load(file)
        return json_data["payload"], json_data["response"]

    return func


@pytest.fixture
def remove_uuid_fields_from_response() -> Callable[[dict], dict]:
    def validate(value):
        type_of_value, value = _get_dict_or_list(value=value)
        return {"list": _change_dict_in_list, "dict": _remove_id_field_in_dict}.get(type_of_value, lambda x: x)(value)

    def _get_dict_or_list(value) -> Tuple[str, Union[list, dict]]:
        type_of_value = type(value).__name__
        dumped_data = loads(dumps(value))
        return {
            "ReturnDict": ("dict", dumped_data),
            "ReturnList": ("list", dumped_data),
        }.get(type_of_value, (type_of_value, value))

    def _change_dict_in_list(root_list: List[dict]) -> List[dict]:
        return [validate(value=value) for value in root_list]

    def _remove_id_field_in_dict(root_dict: dict) -> dict:
        return {key: validate(value=value) for key, value in root_dict.items() if key != "uuid"}

    return validate
