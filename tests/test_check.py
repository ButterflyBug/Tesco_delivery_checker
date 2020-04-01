import pytest
import mock
from datetime import datetime
from check import check


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "decode_compressed_response": True,
        "filter_post_data_parameters": ["email", "password"],
    }


@pytest.mark.vcr()
@mock.patch("check.datetime")
def test_check_no_slots_available(mocked_date):
    mocked_date.now.return_value = datetime(2020, 3, 29)
    assert not check()


@mock.patch("check.SendGridAPIClient")
@mock.patch("check.datetime")
@pytest.mark.vcr()
def test_check_slots_available(mocked_date, mocked_sendgrid_api_client):
    mocked_date.now.return_value = datetime(2020, 3, 29)
    assert check()
