import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect

from api_clients.flight_search_api import get_flight_info
from dark_titlebar import apply_theme_to_titlebar


class travel_planner_app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Planner Application")
        self.geometry('1920x1080')

        self.container=tk.Frame(self)
        self.container.pack(fill="both", expand=True)

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

        departure = tk.Entry(self)
        departure.pack(padx=10)


        label = tk.Label(self, text="Destination")
        label.pack()

        destination = tk.Entry(self)
        destination.pack(padx=10)

        ttk.Button(self,
                   text="Retrieve Flight Offers",
                   width=20,
                   command= lambda: self.controller.show_page(FlightOfferPage)
                   ).pack(pady=10)


class FlightOfferPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller

        self.output_box = tk.Text(self, wrap="word", font=("Courier", 10))
        self.output_box.pack(fill="both", expand=True, padx=10, pady=10)


    def get_flight_offers(self,origin,destination):

        return get_flight_info(origin,destination,"2025-03-17",1)



if __name__ == "__main__":
    app=travel_planner_app()
    app.mainloop()
