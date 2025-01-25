import requests
from decouple import config
from amadeus_conenction import authorize_connection


def get_hotels_id(city_code):
    hotel_search_url=config("HOTEL_SEARCH_TOKEN_URL")
    token = authorize_connection()

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
    hotel_id=get_hotels_id(city_code)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params={
        "hotelIds": hotel_id[0],
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "adults": str(adults),
    }

    response = requests.get(hotel_search_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")


hotel_data = get_hotels("NYC", "2025-01-30", "2025-02-10", 1)




