import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect

from api_clients.flight_search_api import get_flight_info
from dark_titlebar import apply_theme_to_titlebar
from data_coversions.fligth_conversions import flight_code_to_name
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


        # Create a wrapper frame to center all widgets
        frame = ttk.Frame(self)
        frame.grid(row=1, column=100, sticky='nsew')

        # Label for Origin
        label_origin = ttk.Label(frame, text="Origin")
        label_origin.grid(row=2, column=10,padx=300, sticky="nsew")

        # Entry for Origin
        self.departure = ttk.Entry(frame, style="TEntry")
        self.departure.grid(row=4, column=5,padx=100, sticky="nsew")

        # Label for Destination
        label_dest = ttk.Label(frame, text="Destination")
        label_dest.grid(row=6, column=10,padx=300, sticky="nsew")

        # Entry for Destination
        self.destination = ttk.Entry(frame,style="TEntry")
        self.destination.grid(row=20, column=5, sticky="nsew")

        self.controller.shared_data["departure"]=self.departure.get()
        self.controller.shared_data["destination"]=self.destination.get()

        # Button
        ttk.Button(
            frame,
            text="Retrieve Flight Offers",
            width=20,
            command=self.retrieve_flight_offers,
            style="TButton",
        ).grid(row=25, column=5,pady=10,padx=100,sticky="nsew")

    def retrieve_flight_offers(self):
        """Retrieves information from shared data"""
        departure_info = self.departure.get()
        destination_info = self.destination.get()

        self.controller.shared_data['departure'] = departure_info
        self.controller.shared_data['destination'] = destination_info

        self.controller.show_page(FlightOfferPage)


class FlightOfferPage(tk.Frame):
    """Interface for page where Flight Offers are displayed."""
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller

        self.route_label = ttk.Label(self, text="Your route text")
        self.route_label.grid(row=0,column=0,pady=10)

        self.flights_text = tk.Text(
            self,
            font=("Helvetica", 16),
            borderwidth=5,
            width=110,
            height=10,
            wrap="word",
            bg="#2E2E2E",
            relief="raised",
        )

        self.flights_text.grid(row=10, column=0, pady=10,padx=40)


        ttk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_page(InputPage)
        ).grid(row=50,column=0,pady=10)

    def tkraise(self,*args, **kwargs):
        """Overload tkraise function to retrieve shared data"""
        origin=self.controller.shared_data.get("departure")
        destination=self.controller.shared_data.get("destination")
        flight_info=get_flight_info(origin,destination,"2025-04-10",1)

        self.route_label.config(text=f"Flights from {flight_code_to_name(origin)} to {flight_code_to_name(destination)}")
        if not isinstance(flight_info, list):
            self.flights_text.insert("1.0",flight_info)
        else:
            for flight in flight_info:
                self.flights_text.insert("1.0",flight)

        self.flights_text.configure(state="disabled")
        super().tkraise(*args, **kwargs)

if __name__ == "__main__":
    app=travel_planner_app()
    app.mainloop()
