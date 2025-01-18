import requests
from decouple import config
from data_coversions.fligth_conversions import flight_code_to_name


#Connects to the API and returns token
def authorize_connection():

    client_id=config("FLIGHT_API_KEY")
    client_secret=config("FLIGHT_API_SECRET")
    token_url=config("FLIGHT_SEARCH_TOKEN_URL")

    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }


    response=requests.post(token_url, headers=headers, data=data)

    #Check if connection is successful
    if response.status_code == 200:
        token=response.json()["access_token"]
        return token

    return None


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

    if response.status_code==200:
        data=response.json()
        #Check if flight offers are found
        if data["data"] and len(data["data"])>0:
            #Retireve all flights
            for flight in data["data"]:
                #Get the price
                price = flight["price"]["total"]
                itinerary=flight["itineraries"][0]

                # Check if flight has connections
                if len(itinerary["segments"]) > 1:
                    print("Flight with connections")
                else:
                    print("Flight without connections")
                for segment in itinerary["segments"]:

                    #Retireve and print all flight information
                    origin = flight_code_to_name(segment["departure"]["iataCode"])
                    destination = flight_code_to_name(segment["arrival"]["iataCode"])

                    direction=f"{origin} -> {destination}"

                    flight_number = segment["carrierCode"] + segment["number"]
                    #Retrieve Times
                    departure=segment["departure"]["at"]
                    arrival=segment["arrival"]["at"]

                    #Print the info for each flight
                    print(f"Flight Segment: {flight_number}")
                    print(f"{direction}")
                    print(f"Departure Date and Time: {departure} ")
                    print(f"Arrival Date and Time: {arrival} ")
                print(f"Price: €{price}")
                print("")
        #When no error are found
        else:
            print("No flight offers found")
    elif response.status_code==400:
        print("Invalid Input")
    else:
        print(f"Status Code: {response.status_code}")
        print(f"Error Details {response.json()}")
        return




