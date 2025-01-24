from api_clients.flight_search_api import get_flight_info

try:
    origin=input("Give the origin: ")
    destination=input("Give the destination: ")
    departure_date=input("Give the departure date (YYYY-MM-DD): ")
    adults=int(input("Give the number of adults: ") )
    print("")
    array=get_flight_info(origin, destination, departure_date, adults)
    for arr in array:
        print(arr)


except Exception as e:
    print(e)

