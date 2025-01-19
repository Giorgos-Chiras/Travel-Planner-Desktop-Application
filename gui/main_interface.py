import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect

from api_clients.flight_search_api import get_flight_info
from dark_titlebar import apply_theme_to_titlebar
from data_coversions.fligth_conversions import flight_code_to_name


class travel_planner_app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Planner Application")
        self.geometry('1920x1080')

        self.container=tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.shared_data={}
        self.pages={}
        for PageClass in (InputPage,FlightOfferPage):
            page=PageClass(self.container,self)
            self.pages[PageClass]=page
            page.grid(row=0,column=0,sticky="nsew")

        sv_ttk.set_theme(darkdetect.theme())
        apply_theme_to_titlebar(self)

        self.show_page(InputPage)


    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()

class InputPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller


        label = tk.Label(self, text="Origin")
        label.pack()

        self.departure = tk.Entry(self)
        self.departure.pack(padx=10)



        label = tk.Label(self, text="Destination")
        label.pack()

        self.destination = tk.Entry(self)
        self.destination.pack(padx=10)


        ttk.Button(self,
                   text="Retrieve Flight Offers",
                   width=20,
                   command= self.retrieve_flight_offers
                   ).pack(pady=10)


    def retrieve_flight_offers(self):

        departure_info = self.departure.get()
        destination_info = self.destination.get()

        self.controller.shared_data['departure'] = departure_info
        self.controller.shared_data['destination'] = destination_info

        self.controller.show_page(FlightOfferPage)


class FlightOfferPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller

        self.route_label = tk.Label(self, text="")
        self.route_label.place(anchor="center")
        self.route_label.pack(pady=20)

        self.flights_label = tk.Label(self, text="")
        self.flights_label.place(anchor='center')
        self.flights_label.pack(pady=20)

        ttk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_page(InputPage)
        ).pack(pady=10)

    def tkraise(self,*args, **kwargs):
        """Overload tkraise funnction to retrieve shared data"""
        origin=self.controller.shared_data.get("departure")
        destination=self.controller.shared_data.get("destination")
        self.route_label.config(text=f"Flights from {flight_code_to_name(origin)} to {flight_code_to_name(destination)}")
        self.flights_label.config(text=f"{get_flight_info(origin, destination, '2025-04-23', 1)}")
        super().tkraise(*args, **kwargs)




if __name__ == "__main__":
    app=travel_planner_app()
    app.mainloop()
