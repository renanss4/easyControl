import tkinter as tk

class AbreCalendarioWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calendário - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")