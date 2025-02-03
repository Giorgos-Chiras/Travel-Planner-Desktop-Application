import requests
from decouple import config
from data_coversions.fligth_conversions import flight_code_to_airport
from api_clients.amadeus_conenction import authorize_connection
#Retruns the offers for flights
def get_flight_info(origin, destination, departure_date, adults):

    flight_search_url=config("FLIGHT_SEARCH_BASE_URL")
    token=authorize_connection()

    if not token:
        print("Unable to get token")
        return

    headers = {
        "Authorization": f"Bearer {token}"
        }

    payload = {
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDateTimeRange": {
                    "date": departure_date
                },
            }
        ],
        "travelers": [
            {"id": str(i + 1), "travelerType": "ADULT"} for i in range(adults)
        ],
        "sources": ["GDS"],
        "searchCriteria": {
            "maxFlightOffers": 5
        }

        }

    response=requests.post(flight_search_url, headers=headers, json=payload)

    # Initialize an empty string for the output
    flight_info = []

    if response.status_code == 200:
        data = response.json()
        # Check if flight offers are found
        if "data" in data and data["data"]:
            for flight in data["data"]:
                itinerary = flight["itineraries"][0]

                for segment in itinerary["segments"]:
                    flight_number = segment["carrierCode"] + segment["number"]
                    origin_airport = flight_code_to_airport(segment["departure"]["iataCode"])
                    destination_airport = flight_code_to_airport(segment["arrival"]["iataCode"])
                    departure = segment["departure"]["at"]
                    arrival = segment["arrival"]["at"]
                    price = flight["price"]["total"]

                    flight_info.append({
                        "flight_number": flight_number,
                        "origin": origin_airport,
                        "destination": destination_airport,
                        "departure": departure,
                        "arrival": arrival,
                        "price": f"€{price}"
                    })
        else:
            flight_info.append({"error": "No flight offers found"})

        return flight_info






