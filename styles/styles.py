from tkinter import ttk
def apply_styles():

    """Styles used for interface are used here"""
    style = ttk.Style()

    style.configure(
        "TLabel",
        font=("Helvetica", 15, "bold"),
        relief="sunken",
        background="Blue",
    )

    style.configure(
        "TText",
        font=("Helvetica", 16, "bold"),
        borderwidth=5,
        padding=5,
        width=30,
        relief="sunken",
    )

    style.configure(
        "TButton",
        font=("Helvetica", 10, "bold"),
        relief="sunken",
        padding=5,

    )

    style.configure(
        "TEntry",
        relief=""
    )

