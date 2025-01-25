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
        if data["data"] and len(data["data"]) > 0:
            # Retrieve all flights
            for flight in data["data"]:
                formatted_output = ''


                # Get the price
                price = flight["price"]["total"]
                itinerary = flight["itineraries"][0]

                # Check if the flight has connections
                if len(itinerary["segments"]) > 1:
                    formatted_output += "Flight with connections\n"
                else:
                    formatted_output += "Flight without connections\n"

                # Process each flight segment
                for segment in itinerary["segments"]:
                    # Retrieve flight information
                    origin = flight_code_to_airport(segment["departure"]["iataCode"])
                    destination = flight_code_to_airport(segment["arrival"]["iataCode"])
                    direction = f"{origin} -> {destination}"
                    flight_number = segment["carrierCode"] + segment["number"]

                    # Retrieve times
                    departure = segment["departure"]["at"]
                    arrival = segment["arrival"]["at"]

                    # Append the segment details to the output string
                    formatted_output += f"Flight Segment: {flight_number}\n"
                    formatted_output += f"{direction}\n"
                    formatted_output += f"Departure Date and Time: {departure}\n"
                    formatted_output += f"Arrival Date and Time: {arrival}\n\n"

                # Append the price
                formatted_output += f"Price: €{price}\n\n"

                temp_array = [formatted_output]
                flight_info.append(temp_array)
        else:
            flight_info += "No flight offers found\n"

    elif response.status_code == 400:
        input_error = "Invalid Input\n"
        return input_error

    else:
        error= f"Status Code: {response.status_code}\n"
        error += f"Error Details: {response.json()}\n"
        return error

    return flight_info






