import tkinter as tk
import threading
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from day_function import day_function

#Constructs day trading gui, this gui uses the day_function to display the predictions of a Long short-term memory (LTSM)
#model that is used to predict tomorrow's stock price. The last 60 days of real and predicted prices are shown
#in a graph to demonstrate if the model is a good fit for real life

class day_gui(tk.Toplevel):
    def __init__(self, master, ticker_text, stock):
        super().__init__(master)
        self.ticker_text = ticker_text
        self.stock = stock
        self.configure(background="midnight blue")
        self.title("Daily Trading Advice")
        self.geometry("300x30")
        self.pb_widgets()
    
    def pb_widgets(self):
        #Displays progress bar until ML model is trained
        s=Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", troughcolor ='light slate blue', background='pale green')
        self.pb = Progressbar(self, orient=HORIZONTAL, length=300, mode='indeterminate', style="red.Horizontal.TProgressbar")
        self.pb.grid(row=0, column=0, sticky=W, pady=2, columnspan=4)
        #opens seperate thread for the ml model to train in, so as to not freeze the app
        threading.Thread(target=self.tom_price).start()

    def tom_price(self):
        #Calls day_function to get predicted prices
        self.pb.start(10)
        tomorrow_price = day_function.get_tommorrow(self.ticker_text)
        tomorrow_price = tomorrow_price[0][0]
        self.tomorrow_price = "{:.1f}".format(tomorrow_price)
        self.today_price = self.stock.get_current_price()
        #stops progress bar and opens main day_trading window
        self.pb.stop()
        self.day_widgets()

    def day_widgets(self):
        #destroys progress bar window and displays new window containing predictions of the LTSM model
        self.pb.destroy()
        self.geometry("800x550")

        self.tp_label = tk.Label(
            self, text="Tomorrow's Price", background='light slate blue', relief="ridge", borderwidth=2, height=2, width=20)
        self.tp_label.grid(row=0, column=0, columnspan=1, sticky=W)
        self.tp_value = Text(self, height=1, wrap="none", width=70, background='light slate blue')
        self.tp_value.insert(INSERT, f"Today\'s Price: {self.today_price} Tomorrow\'s_price: {self.tomorrow_price}")
        self.tp_value.grid(row=0, column=1, columnspan=2, sticky=W)
        #day_function saves the prediction graph which is called here, mpl graphs cannot be displayed within widgets outside of main thread
        self.img = Image.open("daytrade.png")
        self.img = self.img.resize((800, 500))
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.img_label = tk.Label(self, image=self.tkimage, borderwidth=0)
        self.img_label.grid(row=1, column=0, columnspan=4)

    