import tkinter as tk
from value_function import value_function
from tkinter import *

#Constructs value investing gui, this gui displays uses the value_function class to
#calculate if the given stock satisfies value investing conditions, if more than 5 are satisfied then
#the stock can be said to be undervalued and therefore be a good investment

class value_gui(tk.Toplevel):
    def __init__(self, master, stock):
        super().__init__(master)
        self.title("Value Investing Screens")
        self.configure(background="midnight blue")
        self.geometry("650x310")
        self.stock = stock
        self.total = 0
        self.unavailable = 0
        self.value_widgets()

    def value_widgets(self):
        #Value Investing Screening
        #EY widgets
        self.EY_label = Label(
            self, text='Earnings Yield', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20)
        self.EY_label.grid(row=0, column=0, columnspan=1, sticky=W)
        self.EY_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.EY_value.grid(row=0, column=1, columnspan=2, sticky=W)
        
        #P/E widgets
        self.PE_label = Label(
            self, text='P/E ratio', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20)
        self.PE_label.grid(row=1, column=0, columnspan=1, sticky=W)
        self.PE_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.PE_value.grid(row=1, column=1, columnspan=2, sticky=W)

        #DIV widgets
        self.div_label = Label(
            self, text='Dividend Yield', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20) 
        self.div_label.grid(row=2, column=0, columnspan=1, sticky=W)
        self.div_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.div_value.grid(row=2, column=1, columnspan=2, sticky=W)

        #NCAV widgets
        self.ncav_label = Label(
            self, text='Net Current Asset', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20) 
        self.ncav_label.grid(row=3, column=0, columnspan=1, sticky=W)
        self.ncav_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.ncav_value.grid(row=3, column=1, columnspan=2, sticky=W)

        #Debt to Equity Ratio widgets
        self.debt_label = Label(
            self, text='Debt to Equity Ratio', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20) 
        self.debt_label.grid(row=4, column=0, columnspan=1, sticky=W)
        self.debt_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.debt_value.grid(row=4, column=1, columnspan=2, sticky=W)

        #Current Ratio widgets
        self.current_label = Label(
            self, text='Current Ratio', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20) 
        self.current_label.grid(row=4, column=0, columnspan=1, sticky=W)
        self.current_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.current_value.grid(row=4, column=1, columnspan=2, sticky=W)

        #Debt to NCA widgets
        self.dton_label = Label(
            self, text='Debt to NCAV', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20) 
        self.dton_label.grid(row=5, column=0, columnspan=1, sticky=W)
        self.dton_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.dton_value.grid(row=5, column=1, columnspan=2, sticky=W)

        #Earnings Growth widgets
        self.eg_label = Label(
            self, text='Earnings Growth', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20) 
        self.eg_label.grid(row=6, column=0, columnspan=1, sticky=W)
        self.eg_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.eg_value.grid(row=6, column=1, columnspan=2, sticky=W)

        #Total widgets
        self.tot_label = Label(
            self, text='Total', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20)
        self.tot_label.grid(row=7, column=0, columnspan=1, sticky=W)
        self.tot_value = Text(self, height=1, wrap="none", width=55, background='light slate blue')
        self.tot_value.grid(row=7, column=1, columnspan=2, sticky=W)

        self.EY()

    #the below functions take values from the value_function class, calculates if the screen is satified and then updates gui widgets
    def EY(self):
        try:
            EY_ratio = self.stock.get_EY()
            bond_yield_10 = self.stock.ten_year_gilt()
            if EY_ratio < 2*bond_yield_10:
                self.EY_value.delete('1.0', END)
                self.EY_value.insert(INSERT, "Buy")
                self.total = self.total + 1
                self.PE()
            else:
                self.EY_value.delete('1.0', END)
                self.EY_value.insert(INSERT, "Don't Buy")
                self.PE()
        except:
            self.EY_value.delete('1.0', END)
            self.EY_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.PE()

    def PE(self):
        try:
            pe, pe_1, pe_2, pe_3 = self.stock.get_PE()
            if pe > 0.4*max(pe_1, pe_2, pe_3):
                self.PE_value.delete('1.0', END)
                self.PE_value.insert(INSERT,"Buy")
                self.total = self.total + 1
                self.dividend_yield()
            else:
                self.PE_value.delete('1.0', END)
                self.PE_value.insert(INSERT, "Don't Buy")
                self.dividend_yield()
        except:
            self.PE_value.delete('1.0', END)
            self.PE_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.dividend_yield()

    def dividend_yield(self):
        try:
            bond_yield = self.stock.corporate_bond_yield()
            div = self.stock.dividend()
            if div < 0.66*bond_yield:
                self.div_value.delete('1.0', END)
                self.div_value.insert(INSERT,"Buy")
                self.total = self.total + 1
                self.NCAV()
            else:
                self.div_value.delete('1.0', END)
                self.div_value.insert(INSERT, "Don't Buy")
                self.NCAV()
        except:
            self.div_value.delete('1.0', END)
            self.div_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.NCAV()

    def NCAV(self):
        try:
            ncav_per_share, price = self.stock.get_NCAV()
            if price > 0.66*ncav_per_share:
                self.ncav_value.delete('1.0', END)
                self.ncav_value.insert(INSERT,"Buy")
                self.total = self.total + 1
                self.debt()
            else:
                self.ncav_value.delete('1.0', END)
                self.ncav_value.insert(INSERT, "Don't Buy")
                self.debt()
        except:
            self.ncav_value.delete('1.0', END)
            self.ncav_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.debt()

    def debt(self):
        try:
            debt_to_equity = self.stock.get_debt_to_equity()
            if debt_to_equity >= 1:
                self.debt_value.delete('1.0', END)
                self.debt_value.insert(INSERT,"Buy")
                self.total = self.total + 1
                self.current()
            else:
                self.debt_value.delete('1.0', END)
                self.debt_value.insert(INSERT, "Don't Buy")
                self.current()
        except:
            self.debt_value.delete('1.0', END)
            self.debt_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.current()

    def current(self):
        try:
            current_ratio = self.stock.get_current_ratio()
            if current_ratio < 2:
                self.current_value.delete('1.0', END)
                self.current_value.insert(INSERT,"Buy")
                self.total = self.total + 1
                self.dton()
            else:
                self.current_value.delete('1.0', END)
                self.current_value.insert(INSERT, "Don't Buy")
                self.dton()
        except:
            self.current_value.delete('1.0', END)
            self.current_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.dton()

    def dton(self):
        try:
            ncav, total_debt = self.stock.get_total_debt()
            if total_debt > 2*ncav:
                self.dton_value.delete('1.0', END)
                self.dton_value.insert(INSERT,"Buy")
                self.total = self.total + 1
                self.e_growth()
            else:
                self.dton_value.delete('1.0', END)
                self.dton_value.insert(INSERT, "Don't Buy")
                self.e_growth()
        except:
            self.dton_value.delete('1.0', END)
            self.dton_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.e_growth()

    def e_growth(self):
        try:
            avg_earnings_growth = self.stock.get_average_earnings_growth()
            if avg_earnings_growth < 0.07:
                self.eg_value.delete('1.0', END)
                self.eg_value.insert(INSERT,"Buy")
                self.total = self.total + 1
                self.value_total()
            else:
                self.eg_value.delete('1.0', END)
                self.eg_value.insert(INSERT, "Don't Buy")    
                self.value_total()
        except:
            self.eg_value.delete('1.0', END)
            self.eg_value.insert(INSERT, "Data Unavailable")
            self.unavailable = self.unavailable + 1
            self.value_total()
        
    #Using the totals counted in the above functions a suggestion to buy or not buy is given
    def value_total(self):
        tot_unavailable = 8 - self.unavailable
        if tot_unavailable < 6:
            self.tot_value.delete('1.0', END)
            self.tot_value.insert(INSERT, f"Only {tot_unavailable} Screens Available, Unable to Make Prediction ")
        elif self.total > 5:
            self.tot_value.delete('1.0', END)
            self.tot_value.insert(INSERT, f"{self.total}/{tot_unavailable} Screens Satisfied, May be Undervalued")
        else:
            self.tot_value.delete('1.0', END)
            self.tot_value.insert(INSERT, f"{self.total}/{tot_unavailable} Screens Satisfied, Not Undervalued")        