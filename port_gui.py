import tkinter as tk
from tkinter import *
from tkinter import ttk

import numpy as np
import PIL
from PIL import Image, ImageTk
from port_function import port_function
from db import Database
import matplotlib.pyplot as plt

#Constructs portfolio management gui, this calls the port_function class to populate the a new tkinter window
#with a .png of the efficient frontier of the current portfolio aswell as a database of the current stocks and weightings.
#This also has the functionality to add and remove items from the sqlite database using db.py

class port_gui(tk.Toplevel):
    def __init__(self, master, ticker_text):
        super().__init__(master)
        self.ticker = ticker_text.upper()
        self.title("Portfolio Management")
        self.configure(background="midnight blue")
        self.geometry("800x600")
        self.db = Database('port.db')
        self.port_widgets()

    def port_widgets(self):
        
        #Adds ticker entry box that is populated by the ticker entry of the main page
        self.ticker_text = tk.StringVar()
        self.ticker_label = tk.Label(self, text='Ticker Entry: ', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20)
        self.ticker_label.grid(row=0, column=0, pady=2, sticky=W)
        self.ticker_entry = tk.Entry(self, textvariable=self.ticker_text, background='light slate blue', width=20)
        self.ticker_entry.insert(END, self.ticker)
        self.ticker_entry.grid(row=0,column=1, pady = 2)

        #Add Button
        self.add_btn = tk.Button(self, text="Add Stock?", width=20, height=2, command=self.add_item, background='light slate blue')
        self.add_btn.grid(row=0, column=2, sticky=W, pady=2)

        #Generate Optimum Risky Portfolio
        self.add_btn = tk.Button(self, text=f"Optimum Portfolio", width=20, height=2, command=self.gen_port, background='light slate blue')
        self.add_btn.grid(row=0, column=3, sticky=W, pady=2)
        
        #set style for scrollbar
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar", background="midnight blue", bordercolor="light slate blue", arrowcolor="white", troughcolor="light slate blue")

        #Portfolio Database
        frame = tk.Frame(self)
        frame.grid(row=1, column=0, columnspan=1, rowspan=3, sticky=N)
        self.stock_list = tk.Listbox(frame, height=22, width=20, borderwidth=0, highlightthickness=0, bg="light slate blue")
        self.stock_list.pack(side='left', fill='y')
        self.scrollbar = ttk.Scrollbar(frame, orient=VERTICAL)
        self.scrollbar.pack(side='right', fill='y')
        self.stock_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.stock_list.yview)
        self.populate_list()
        
        #Open saved efficient frontier png
        self.img = Image.open("portfolio.png")
        self.img = self.img.resize((640, 400))
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.img_label = tk.Label(self, image=self.tkimage, borderwidth=0)
        self.img_label.grid(row=1, column=1, columnspan=3, rowspan=3)

        #Remove Button
        self.remove_btn = tk.Button(self, text="Remove", width=20, height=2, command=self.remove_item, background='light slate blue')
        self.remove_btn.grid(row=3, column=0, sticky=S, pady=2)

        #Arithmetic Mean
        self.avg_return = tk.Label(self, text="Mean Returns: ", width=20, height=2, background='light slate blue', relief="ridge", borderwidth=2, pady=2)
        self.avg_return.grid(row=5, column=0, columnspan=1)
        self.avg_return_text = tk.Text(self, height=1, wrap="none", width=20, background='light slate blue', font = ('Verdana', 10))
        self.avg_return_text.grid(row=5, column=1)

        #Standard Deviation
        self.std_label = tk.Label(self, text="Volatility: ", width=20, height=2, background='light slate blue', relief="ridge", borderwidth=2, pady=2)
        self.std_label.grid(row=5, column=2, columnspan=1)
        self.std_text = tk.Text(self, height=1, wrap="none", width=20, background='light slate blue', font = ('Verdana', 10))
        self.std_text.grid(row=5, column=3, sticky=W)

        #Sharpe Ratio
        self.sharpe_label = tk.Label(self, text="Sharpe Ratio: ", width=20, height=2, background='light slate blue', relief="ridge", borderwidth=2, pady=2)
        self.sharpe_label.grid(row=6, column=0, columnspan=1)
        self.sharpe_text = Text(self, height=1, wrap="none", width=20, background='light slate blue', font = ('Verdana', 10))
        self.sharpe_text.grid(row=6, column=1)

        #Information Ratio
        self.info_label = tk.Label(self, text="Information Ratio: ", width=20, height=2, background='light slate blue', relief="ridge", borderwidth=2, pady=2)
        self.info_label.grid(row=6, column=2, columnspan=1)
        self.info_text = tk.Text(self, height=1, wrap="none", width=20, background='light slate blue', font = ('Verdana', 10))
        self.info_text.grid(row=6, column=3, sticky=W)
   
    
    def add_item(self):
        #Adds stock from entry field to sqlite database using db.py
        self.db.insert(self.ticker_text.get(), "%")
        self.populate_list()

    def remove_item(self):
        #Removes selected stock from database using db.py
        index = self.stock_list.curselection()[0]
        selected_item = self.stock_list.get(index)
        self.db.remove(selected_item[0])
        self.populate_list()

    def populate_list(self):
        #Clears database and repopulates it with new efficient weightings
        self.stock_list.delete(0, END)
        for row in self.db.fetch():
            self.stock_list.insert(END, row)

    def gen_port(self):
        #Uses port_function to populate new efficient frontier, also populates analysis widgets
        portfolios = port_function()
        max_sharpe_allocation, rp, sdp, sharpe_ratio= portfolios.max_sharpe()

        rows = self.db.fetch()
        for each in rows:
            self.db.remove(each[0])

        for each in max_sharpe_allocation:
            self.db.insert(each, max_sharpe_allocation[each]['allocation'])

        self.populate_list()
        #Information ratio compares the sharpe ratio against the return of an index fund
        mean_ftse_returns, std_ftse_returns = portfolios.ftse_stats()
        information_ratio = (rp-mean_ftse_returns)/(sdp-std_ftse_returns)

        #Updates analysis widgets with new efficient frontier stats
        self.avg_return_text.delete('1.0', END)
        self.avg_return_text.insert(INSERT, rp)
        self.std_text.delete('1.0', END)
        self.std_text.insert(INSERT, sdp)
        self.sharpe_text.delete('1.0', END)
        self.sharpe_text.insert(INSERT, sharpe_ratio)
        self.info_text.delete('1.0', END)
        self.info_text.insert(INSERT, information_ratio)

        self.show_ef()

    def show_ef(self):
        #updates graph label with new saved png
        portfolios = port_function()
        portfolios.get_ef()
        self.img = Image.open("portfolio.png")
        self.img = self.img.resize((640, 400))
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.img_label.configure(image=self.tkimage)