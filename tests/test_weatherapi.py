import pytest
from unittest.mock import patch, Mock
from website.utils import WeatherAPI


@pytest.fixture
def weather_api():
    """Fixture to provide a WeatherAPI instance."""
    return WeatherAPI()


@patch("requests.request")
def test_getCurrentWeather_success(mock_request, weather_api):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"condition": {"text": "Sunny"}}
    mock_request.return_value = mock_response

    city = "Raleigh"
    result = weather_api.getCurrentWeather(city=city)
    assert result == "Sunny"
    mock_request.assert_called_once_with(
        "GET",
        f"http://api.weatherapi.com/v1/current.json?key={weather_api.config.API_KEY}&q={city}&aqi=no",
        headers={},
        data={}
    )


@patch("requests.request")
def test_getCurrentWeather_failure(mock_request, weather_api):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_request.return_value = mock_response

    city = "InvalidCity"
    with pytest.raises(Exception, match="Weather API failed : response code : 404"):
        weather_api.getCurrentWeather(city=city)


def test_weather_api_call_status_code():
    import requests  # Directly import requests for the API call

    # Example API call details (replace placeholders with actual values)
    city = "Raleigh"
    date = "2024-11-27"
    api_key = "DHEGFSBQJM29A8NAYG98MF67Q" 
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date}?key={api_key}"

    response = requests.get(url)

    # Check if the status code is 200
    assert response.status_code == 200


@patch("requests.request")
def test_getFutureWeather_failure(mock_request, weather_api):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_request.return_value = mock_response

    city = "Raleigh"
    date = "2024-11-27"
    time = "11:00"
    with pytest.raises(Exception, match="Weather API failed : response code : 500"):
        weather_api.getFutureWeather(city=city, date=date, time=time)

