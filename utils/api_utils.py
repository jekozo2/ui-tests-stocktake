import logging
import random
from datetime import date

import requests
from requests import Response

from tests.conftest import BASE_URL

CREATE_SUPPLIER_ENDPOINT = "/items/suppliers"
CREATE_TYPE_ENDPOINT = "/items/product-types"
CREATE_UNIT_ENDPOINT = "/items/product-units"
CREATE_GROUP_ENDPOINT = "/items/product-groups"
CREATE_PRODUCT_ENDPOINT = "/items/products"
CREATE_PURCHASE_ENDPOINT = "/items/purchases"


def create_new_supplier_via_api_call(auth_headers, payload: dict = None) -> Response:
    if payload is None:
        payload = {
            "name": f"Test_supplier_{random.randint(100000, 999999)}",
            "email": f"supplier_email_{random.randint(100000, 999999)}@gmail.com"
        }

    return send_post_request(auth_headers, payload, CREATE_SUPPLIER_ENDPOINT)


def create_new_type_via_api_call(auth_headers, payload: dict = None) -> Response:
    if payload is None:
        payload = {
            "name": f"Test_type_{random.randint(100000, 999999)}",
            "description": f"Description for type {random.randint(100000, 999999)}"
        }

    return send_post_request(auth_headers, payload, CREATE_TYPE_ENDPOINT)


def create_new_unit_via_api_call(auth_headers, payload: dict = None) -> Response:
    if payload is None:
        payload = {
            "name": f"Test_unit_{random.randint(100000, 999999)}",
            "yield_amount": float(random.randint(1, 10)),
            "description": f"Description for unit {random.randint(100000, 999999)}"
        }

    return send_post_request(auth_headers, payload, CREATE_UNIT_ENDPOINT)


def create_new_group_via_api_call(auth_headers, payload: dict = None) -> Response:
    if payload is None:
        payload = {
            "name": f"Test_group_{random.randint(100000, 999999)}",
            "description": f"Description for group {random.randint(100000, 999999)}"
        }

    return send_post_request(auth_headers, payload, CREATE_GROUP_ENDPOINT)


def create_new_product_via_api_call(auth_headers, payload: dict) -> Response:
    return send_post_request(auth_headers, payload, CREATE_PRODUCT_ENDPOINT)


def send_post_request(auth_headers, payload, endpoint: str, path_params: dict = None):
    """
    Send a POST request to the specified API endpoint using data from the context.
    Optionally include dynamic path parameters.

    :param auth_headers: Dictionary containing authentication headers.
    :param payload: The request payload and where the response will be stored.
    :param endpoint: API endpoint key used to look up the base endpoint path in self.ENDPOINTS.
    :param path_params: Dictionary of optional path parameters to inject into the endpoint URL.
    :return: None. The response is stored in context.response.
    """
    base_path = endpoint
    if path_params:
        try:
            base_path = endpoint.format(**path_params)
        except KeyError as e:
            raise ValueError(f"Missing path parameter: {e}")

    logging.info(f"Sending POST request to create {base_path}.")
    url = f"{BASE_URL}{base_path}"

    if payload is not None:
        for key, value in payload.items():
            if isinstance(value, date):
                payload[key] = value.strftime("%Y-%m-%d")

    response = requests.post(url, headers=auth_headers, json=payload)

    logging.debug(
        f"""
    RESPONSE BODY =========================================================
    Endpoint: {base_path}
    Status code: {response.status_code}
    Response Text: {response.text}
    ======================================================================
    """
    )

    return response
