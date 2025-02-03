import requests
from decouple import config
from amadeus_conenction import authorize_connection


def get_hotels_id(city_code):
    #Set API url and get token
    hotel_search_url=config("HOTEL_SEARCH_TOKEN_URL")
    token = authorize_connection()

    #Check if token is valid
    if not token:
        print("Unable to get token")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
        }

    params = {
        "cityCode": city_code,
    }

    response = requests.get(hotel_search_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        hotel_id=[]

        for hotel in data["data"]:
            hotel_id.append(hotel["hotelId"])

        return hotel_id

    else:
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")

def get_hotels(city_code,check_in_date, check_out_date, adults):
    hotel_search_url=config("HOTEL_SEARCH_OFFERS_TOKEN_URL")
    token = authorize_connection()

    if not token:
        print("Unable to get token")
        return

    #Get IDs of hotel by city
    hotel_id=get_hotels_id(city_code)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    #Only get offers for 5 hotels
    hotel_id=hotel_id[:5]

    #Set the parameters to the one passed by user
    params={
        "hotelIds": hotel_id,
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "adults": str(adults),
    }

    #Generate the response
    response = requests.get(hotel_search_url, headers=headers, params=params)

    #Check if response is valid and print details if it is
    if response.status_code == 200:
        data = response.json()

        for hotel_data in data.get("data", []):
            hotel = hotel_data.get("hotel", {})
            print(f"Hotel ID: {hotel.get('hotelId')}")
            print(f"Hotel Name: {hotel.get('name')}")
            print("\nOffers")

            for offers in hotel_data.get("offers", []):
                print(f"Offer ID: {offers.get('id')}")
                print(f"Check in Date: {offers.get('checkInDate')}")
                print(f"Check out Date: {offers.get('checkOutDate')}")
                print(f"Description: {(offers.get('description', {})).get('text')}")


                room_info = offers.get("room", {})
                print(f"Room Type: {room_info.get('type')}")
                print(f"Room Description: {room_info.get('description', {}).get('text')}")

                price_info=offers.get('price',{})
                print(f"Price Type: {price_info.get('currency')} {price_info.get('total')}")

            print("\n")

    else:
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")


get_hotels("NYC", "2025-03-05", "2025-03-10", 1)




