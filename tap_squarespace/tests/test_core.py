"""Tests standard tap features using the built-in SDK tests library."""

import datetime

import pytest
from hotglue_etl_exceptions import InvalidPayloadError
from hotglue_singer_sdk.exceptions import FatalAPIError
from hotglue_singer_sdk.testing import get_standard_tap_tests
from requests import Response

from tap_squarespace.streams import OrdersStream
from tap_squarespace.tap import Tapsquarespace

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    # TODO: Initialize minimal tap config
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        Tapsquarespace,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()


def _response(status_code: int, reason: str) -> Response:
    """Build an API response with the requested status."""
    response = Response()
    response.status_code = status_code
    response.reason = reason
    response.url = "https://api.squarespace.com/1.0/commerce/orders"
    return response


def test_orders_payment_required_is_invalid_payload():
    """A commerce-orders payment requirement is a configuration error."""
    stream = object.__new__(OrdersStream)

    with pytest.raises(
        InvalidPayloadError,
        match="402 Client Error: Payment Required for path: /1.0/commerce/orders",
    ):
        stream.validate_response(_response(402, "Payment Required"))


def test_orders_success_response_is_accepted():
    """Successful commerce-orders responses retain SDK behavior."""
    stream = object.__new__(OrdersStream)

    assert stream.validate_response(_response(200, "OK")) is None


def test_orders_other_client_errors_remain_fatal():
    """Only payment-required responses change classification."""
    stream = object.__new__(OrdersStream)

    with pytest.raises(FatalAPIError, match="401 Client Error"):
        stream.validate_response(_response(401, "Unauthorized"))
