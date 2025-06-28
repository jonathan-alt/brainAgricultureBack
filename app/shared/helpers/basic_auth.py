import base64
import requests
from typing import Tuple


def get_authorization_scheme_param(authorization_header_value: str) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


def get_token_from_headers(headers: dict) -> str:
    authorization_header_value = headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization_header_value)
    if not authorization_header_value or scheme.lower() != "token":
        return ""

    return param


def generate_basic_auth_headers(client_id, secret_id):
    client_id = client_id.encode("utf-8")
    client_secret = secret_id.encode("utf-8")

    basic_auth = base64.b64encode(client_id + b":" + client_secret)
    headers = {
        "Authorization": "Basic {}".format(basic_auth.decode("utf-8")),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    return headers
