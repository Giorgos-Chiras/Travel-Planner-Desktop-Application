import tkinter as tk
from tkinter import ttk
import requests
import json
import sv_ttk
import darkdetect
from dark_titlebar import apply_theme_to_titlebar


def get_entry_text(destination):

    return destination.get()

def main():

    root = tk.Tk()
    root.title('Travel Planner Application')
    root.geometry('1920x1080')

    label = tk.Label(root, text="Departure")
    label.pack()

    departure = tk.Entry(root)
    departure.pack(padx=10)

    ttk.Button(root,
               text="Submit",
               width=20,
               command=lambda: get_entry_text(departure)).pack(pady=10)

    label= tk.Label(root, text="Destination")
    label.pack()

    destination=tk.Entry(root)
    destination.pack(padx=10)

    ttk.Button(root,
               text="Submit",
               width=20,
               command=lambda: get_entry_text(destination)).pack(pady=10)

    sv_ttk.set_theme(darkdetect.theme())

    apply_theme_to_titlebar(root)
    root.mainloop()


if __name__ == "__main__":
    main()
