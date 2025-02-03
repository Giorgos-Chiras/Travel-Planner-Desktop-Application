import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect

from api_clients.flight_search_api import get_flight_info
from dark_titlebar import apply_theme_to_titlebar
from data_coversions.fligth_conversions import *
from styles.styles import apply_styles


class travel_planner_app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Planner Application")
        self.geometry('1920x1080')

        sv_ttk.set_theme(darkdetect.theme())
        apply_theme_to_titlebar(self)
        apply_styles()


        self.container=tk.Frame(self)
        self.container.grid(row=0, column=0)

        self.shared_data={}
        self.pages={}

        for PageClass in (InputPage,FlightOfferPage):
            page=PageClass(self.container,self)
            self.pages[PageClass]=page
            page.grid(row=0,column=0,sticky="nsew")


        self.show_page(InputPage)


    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()


class InputPage(tk.Frame):
        def __init__(self, parent, controller):
            """Interface for page where user enters input"""
            super().__init__(parent)
            self.controller = controller

            # Configure grid layout for the parent frame
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            # Create a wrapper frame to center all widgets
            frame = ttk.Frame(self, padding=20)
            frame.grid(row=0, column=0, sticky="nsew")

            # Configure grid layout for the frame
            frame.grid_rowconfigure(tuple(range(10)), weight=1)
            frame.grid_columnconfigure(0, weight=1)

            # Label for Origin
            label_origin = ttk.Label(frame, text="Origin", anchor="center")
            label_origin.grid(row=0, column=0, pady=10)

            # Entry for Origin
            self.departure = ttk.Entry(frame, justify="center")
            self.departure.grid(row=1, column=0, pady=5)

            # Label for Destination
            label_dest = ttk.Label(frame, text="Destination", anchor="center")
            label_dest.grid(row=2, column=0, pady=10)

            # Entry for Destination
            self.destination = ttk.Entry(frame, justify="center")
            self.destination.grid(row=3, column=0, pady=5)

            # Label for Departure Date
            departure_date_label = ttk.Label(frame, text="Departure Date", anchor="center")
            departure_date_label.grid(row=4, column=0, pady=10)

            # Entry for Departure Date
            self.departure_date = ttk.Entry(frame, justify="center")
            self.departure_date.grid(row=5, column=0, pady=5)

            # Label for Return Date
            return_date_label = ttk.Label(frame, text="Return Date", anchor="center")
            return_date_label.grid(row=6, column=0, pady=10)

            # Entry for Return Date
            self.return_date = ttk.Entry(frame, justify="center")
            self.return_date.grid(row=7, column=0, pady=5)

            # Label for Return Date
            adults_label = ttk.Label(frame, text="Number of Adults", anchor="center")
            adults_label.grid(row=8, column=0, pady=10)

            # Entry for Number of Adults
            self.adults = ttk.Spinbox(frame,from_=1, to=10,state='readonly', justify="center")
            self.adults.grid(row=9, column=0, pady=5)

            # Update shared data
            self.controller.shared_data["departure"] = self.departure.get()
            self.controller.shared_data["destination"] = self.destination.get()
            self.controller.shared_data["departure_date"] = self.departure_date.get()
            self.controller.shared_data["return_date"] = self.return_date.get()
            self.controller.shared_data["adults"] = self.adults.get()

            # Button
            retrieve_button = ttk.Button(
                frame,
                text="Retrieve Flight Offers",
                command=self.retrieve_flight_offers
            )
            retrieve_button.grid(row=10, column=0, pady=20)

        def retrieve_flight_offers(self):
            """Retrieves information from shared data"""
            departure_info = self.departure.get()
            destination_info = self.destination.get()
            departure_date = self.departure_date.get()
            return_date = self.return_date.get()
            adults=self.adults.get()

            self.controller.shared_data['departure'] = departure_info
            self.controller.shared_data['destination'] = destination_info
            self.controller.shared_data['departure_date'] = departure_date
            self.controller.shared_data['return_date'] = return_date
            self.controller.shared_data['adults']=int(adults)

            self.controller.show_page(FlightOfferPage)

class FlightOfferPage(tk.Frame):
    """Interface for page where Flight Offers are displayed."""
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller

        self.route_label = ttk.Label(self, text=" ")
        self.route_label.grid(row=0,column=0,pady=10)

        self.date_label = ttk.Label(self, text=" ")
        self.date_label.grid(row=1,column=0,pady=10)

        columns = ("Flight Number", "Origin", "Destination", "Departure", "Arrival", "Price")
        self.flights_table = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        # Define column headers
        for col in columns:
            self.flights_table.heading(col, text=col)
            self.flights_table.column(col, width=120)

        self.flights_table.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        ttk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_page(InputPage)
        ).grid(row=50,column=0,pady=10)

    def tkraise(self,*args, **kwargs):
        """Overload tkraise function to retrieve shared data"""

        #Get shared data
        origin=self.controller.shared_data.get("departure")
        destination=self.controller.shared_data.get("destination")
        departure_date=self.controller.shared_data.get("departure_date")
        return_date=self.controller.shared_data.get("return_date")
        adults=self.controller.shared_data.get("adults")

        flights=get_flight_info(origin,destination,departure_date,adults)

        self.route_label.config(text=f"Flights from {flight_code_to_city(origin)} to {flight_code_to_city(destination)}")
        self.date_label.config(text=f"From {departure_date} to {return_date} for {adults} adults")

        #Check whether we returned list or string
        if flights:
            for flight in flights:

                flight_number = flight["flight_number"]
                origin = flight["origin"]
                destination = flight["destination"]
                departure = flight["departure"]
                arrival = flight["arrival"]
                price = flight["price"]

                self.flights_table.insert("", "end",
                values=(flight_number, origin, destination, departure, arrival, price))

        super().tkraise(*args, **kwargs)


if __name__ == "__main__":
    app=travel_planner_app()
    app.mainloop()
