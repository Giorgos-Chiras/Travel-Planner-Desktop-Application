import csv

def flight_code_to_airport(airport_code):
   with open('../resources/airports.csv', mode='r', encoding='utf-8') as file:
       csvFile = csv.DictReader(file)
       for row in csvFile:
           iata_codes=row['iata_code']
           airport_name=row['name']

           if iata_codes == airport_code:
                return airport_name

       return "No airport found"

def flight_code_to_city(airport_code):
    airport=flight_code_to_airport(airport_code)
    return airport.split()[0]
