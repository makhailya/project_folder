from unittest.mock import patch, MagicMock
from src.api.hh_api import HeadHunterAPI


@patch("src.api.hh_api.requests.Session")
def test_hh_api_get_vacancies_success(mock_session):
    fake_resp = MagicMock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = {"items": [{"id": "1"}, {"id": "2"}]}
    mock_session.return_value.get.return_value = fake_resp

    api = HeadHunterAPI()
    result = api.get_vacancies("Python")
    assert isinstance(result, list)
    assert len(result) == 2
    mock_session.return_value.get.assert_called()
