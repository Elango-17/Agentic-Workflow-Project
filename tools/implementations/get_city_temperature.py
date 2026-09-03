from typing import Any, Dict
import requests
from tools.base import BaseTool


class GetCityTemperature(BaseTool):
    """Tool to retrieve the current temperature for a specified city using Open-Meteo's free weather API."""

    def execute(self, city: str) -> Dict[str, Any]:
        """Retrieves the current temperature for the specified city.

        Args:
            city: The name of the city for which to retrieve the temperature.

        Returns:
            A dictionary containing the current temperature and temperature unit.
        """
        if not city or not isinstance(city, str) or not city.strip():
            raise ValueError("The 'city' parameter must be a non-empty string.")

        city_name = city.strip()

        # Step 1: Geocode the city name to get latitude and longitude using Open-Meteo geocoding API
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city_name, "count": 1, "language": "en", "format": "json"}

        try:
            geo_response = requests.get(geocoding_url, params=geo_params, timeout=10)
            geo_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to the geocoding service: {e}")

        geo_data = geo_response.json()
        results = geo_data.get("results")

        if not results:
            raise ValueError(f"Could not find geographic coordinates for city: '{city_name}'")

        location = results[0]
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        resolved_city_name = location.get("name", city_name)
        country = location.get("country", "")

        # Step 2: Retrieve current weather using the coordinates
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "temperature_unit": "celsius"
        }

        try:
            weather_response = requests.get(weather_url, params=weather_params, timeout=10)
            weather_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to the weather service: {e}")

        weather_data = weather_response.json()
        current = weather_data.get("current")

        if not current or "temperature_2m" not in current:
            raise RuntimeError(f"Temperature data is not available for '{resolved_city_name}'.")

        temperature = current["temperature_2m"]
        temperature_unit = weather_data.get("current_units", {}).get("temperature_2m", "°C")

        return {
            "city": resolved_city_name,
            "country": country,
            "temperature": temperature,
            "unit": temperature_unit
        }
