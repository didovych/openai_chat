import os
import requests
from dotenv import load_dotenv

# Conversation examples:

# Can you calculate a footprint for my family vacation flight?
# We will fly from Amsterdam to Madrid with my wife

class CarbonFootprint:
    def __init__(self):
        self.base_url = "https://www.carboninterface.com/api/v1/"
        # read the API key from the environment variable
        load_dotenv()
        self.api_key = os.environ.get("CARBON_API_KEY")
        self.system_prompt = """
            You are an assistant for the carbon footprint calculation.
        """

    def get_electricity_footprint(self, electricity_value: float, country: str) -> float:
        """
        Get electricity carbon footprint in kgCO2e.

        Args:
            electricity_value (float): The electricity value in megawatt-hours (MWh).
            country (str): The country's ISO 3166 code.
        Returns:
            float: The carbon footprint in kgCO2e.
        """

        print(f"Log: get_electricity_footprint called with electricity_value: {electricity_value} and country: {country}")

        data = {
            "type": "electricity",
            "electricity_unit": "mwh",
            "electricity_value": electricity_value,
            "country": country
        }

        return self.__make_api_request(data)

    def get_flight_footprint(self, departure_airport: str, destination_airport: str, passengers: int) -> float:
        """
        Get flight carbon footprint in kgCO2e.

        Args:
            departure_airport (str): The departure airport IATA code. For example, "sfo".
            destination_airport (str): The destination airport IATA code. For example, "jfk".
            passengers (int): The number of passengers.
        Returns:
            float: The carbon footprint in kgCO2e.
        """

        print(f"Log: get_flight_footprint called with departure_airport: {departure_airport}, destination_airport: {destination_airport}, and passengers: {passengers}")

        data = {
            "type": "flight",
            "passengers": passengers,
            "legs": [
                {
                    "departure_airport": departure_airport,
                    "destination_airport": destination_airport
                }
            ]
        }

        return self.__make_api_request(data)

    def __make_api_request(self, data: dict) -> float:
        url = f"{self.base_url}estimates"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            carbon_kg = result.get("data", {}).get("attributes", {}).get("carbon_kg", 0.0)
            print(f"Log: carbon_kg: {carbon_kg}")
            return carbon_kg
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return 0.0