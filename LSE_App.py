from port_gui import port_gui
from day_gui import day_gui
from value_gui import value_gui
from value_function import value_function

from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

import yfinance as yf
import mplfinance as mpf
import tkinter as tk

def main():
    class Application(tk.Frame):
        def __init__(self, master):
            #constructor
            super().__init__(master)
            self.master = master
            self.master.configure(background="midnight blue")
            master.title('London Stock Exchange Analysis App')
            master.geometry("800x650")
            self.main_gui()
            
        def main_gui(self):

            #scrolling ticker
            ##formatting
            self.ticker = tk.Text(height=1, wrap="none")
            self.ticker.configure(background="black")
            self.ticker.grid(row=0, column=0, columnspan=3, sticky=W, pady = 2) 
            ##colour
            self.ticker.tag_configure("up", foreground="green")
            self.ticker.tag_configure("down", foreground="red")
            self.ticker.tag_configure("even", foreground="white")
            ##calling methods
            self.data = self.get_data()
            self.tick()

            #market label
            self.market = tk.Text(height=1, wrap="none", width="18")
            self.market.grid(row=0, column=3 ,sticky=W, pady = 2) 
            self.get_market()

            #ticker label
            self.ticker_text = tk.StringVar()
            self.ticker_label = tk.Label(
                self.master, text='Ticker Entry: ', background='light slate blue', relief="ridge", pady=2, borderwidth=2, height=2, width=20) #pady=20 font=('bold', 12)
            self.ticker_label.grid(row=1, column=0, pady = 2, sticky=W) #sticky

            #ticker entry box
            self.ticker_entry = tk.Entry(self.master, textvariable=self.ticker_text, background='light slate blue', font = ('Verdana', 10))
            self.ticker_entry.grid(row=1,column=1, sticky=W, pady = 2)

            #period entry
            self.period_text = tk.StringVar(self.master)
            self.period_text.set("1 Year")
            self.period_entry = tk.OptionMenu(self.master, self.period_text, "1 Year", "1 Day", "5 Days", "1 Month", "3 Months", "6 Months", "2 Years", "5 Years", "10 Years" , "Year to Date" , "Maximum")
            self.period_entry.configure(background='light slate blue', width=20, highlightthickness=0)
            self.period_entry["menu"].configure(bg='light slate blue')
            self.period_entry.grid(row=1, column=2, sticky=W, pady = 2)

            #Generate button        
            self.ticker_btn = tk.Button(
                self.master, text="Generate", width=12, command=self.gen_graph, background='light slate blue')
            self.ticker_btn.grid(row=1,column=3, sticky=W, pady = 2)

            #creating canvas for graphs
            self.fig = Figure(figsize=(8,5), dpi=100)
            self.fig.set_facecolor('midnightblue')
            canvas = FigureCanvasTkAgg(self.fig, master = self.master)
            #adding canvas to gui
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=0, columnspan=8, sticky=W, pady = 2)

            #function button labels
            self.function_label = tk.Label(self.master, text="Function Buttons: ", width=20, height=2, background='light slate blue', relief="ridge", borderwidth=2, pady=2)

            #value invest button
            self.value_btn = tk.Button(self.master, text="Value Invest", width=20, height=2, command=self.value_gui, background='light slate blue')

            #tomorrow price button
            self.day_btn = tk.Button(self.master, text="Day Trade", width=20, height=2, command=self.day_gui, background='light slate blue')

            #portfolio button
            self.port_btn = tk.Button(self.master, text="Manage Portfolio", width=20, height=2, command=self.port_gui, background='light slate blue')

        def value_gui(self):
            #Calls value investing gui
            window = value_gui(self, self.stock)
            window.grab_set()

        def day_gui(self):
            #Calls day trading gui
            window = day_gui(self, self.ticker_text.get(), self.stock)
            window.grab_set()
                
        def port_gui(self):
            #Calls portfolio management gui
            window = port_gui(self, self.ticker_text.get())
            window.grab_set()
            
        def tick(self):
            #getting and removing first tuple from dataset
            symbol = self.data.pop(0)
            self.data.append(symbol)
            #getting price change from tuple
            n = symbol[1]
            
            #applying colour on -ve/+ve price change
            if n<0:
                tag = "down"
            elif n>0:
                tag = "up"
            else:
                tag = "even"

            #configuring text
            self.ticker.configure(state="normal")
            self.ticker.insert("end", " %s %s" % (symbol[0], n), tag)
            self.ticker.see("end")
            self.ticker.configure(state="disabled")

            now = datetime.now()
            current_time = now.strftime("%M:%S")

            #Renew the data each half an hour to minimise API calls
            if current_time == "01:01" or current_time == "31:01":
                print("Renewing data")
                self.data = self.get_data()
                print("Renewing data")
                self.after(1010, self.tick)
            else:
                self.after(1000, self.tick)
        
        def get_data(self):
            #creating lists
            tuple_list = []
            FTSE_tickers = ("^FTSE III.L ABDN.L ADM.L AAL.L ANTO.L AHT.L ABF.L AZN.L AUTO.L AVST.L AVV.L AV.L BME.L BA.L BARC.L BDEV.L BKG.L BHP.L BP.L BATS.L BLND.L BT-A.L BNZL.L BRBY.L CCH.L CPG.L CRH.L CRDA.L DCC.L DGE.L SMDS.L ENT.L EVR.L EXPN.L FERG.L FLTR.L FRES.L GSK.L GLEN.L HLMA.L HL.L HIK.L HSBA.L IHG.L IMB.L INF.L ICP.L IAG.L ITRK.L ITV.L JD.L JMAT.L JET.L KGF.L LAND.L LGEN.L LLOY.L LSEG.L MNG.L MRO.L MNDI.L NG.L NWG.L NXT.L OCDO.L PSON.L PSH.L PSN.L PHNX.L POLY.L PRU.L RKT.L REL.L RTO.L RMV.L RIO.L RR.L RDSA.L RMG.L SGE.L SBRY.L SDR.L SMT.L SGRO.L SVT.L SN.L SMIN.L SKG.L SPX.L SSE.L STJ.L STAN.L TW.L TSCO.L ULVR.L UU.L VOD.L WEIR.L WTB.L WPP.L ")
            FTSE_tickers_list = FTSE_tickers.split()

            #downloading full dataset
            full_tickDf = yf.download(tickers = FTSE_tickers, period = "2d", interval="1d", group_by='ticker')

            #populating return list
            for ticker in FTSE_tickers_list:
                tickDf = full_tickDf[ticker]
                yesterday_close = tickDf.iloc[0, tickDf.columns.get_loc('Close')]
                today_latest = tickDf.iloc[1, tickDf.columns.get_loc('Close')]
                price_change = round((today_latest-yesterday_close), 2)
                tuple_list.append((ticker, price_change))

            return (tuple_list)

        def get_market(self):
            #checks if london stock exchange is activly trading every second
            now = datetime.now()
            
            if (now.isoweekday() in range(1,6)) & (now.hour*60+now.minute in range(8*60, 16*60+30)):
                self.market.delete('1.0', END)
                self.market.configure(state="normal", background="green")
                self.market.insert(INSERT, "Market Open")
            else:
                self.market.delete('1.0', END)
                self.market.configure(state="normal", background="red")
                self.market.insert(INSERT, "Market Closed")
            
            self.after(1000, self.get_market)
                
        def gen_graph(self):

            #return error if entry field empty
            if self.ticker_text.get() == '':
                tk.messagebox.showerror("Required Fields", "Please include all fields")
                return
            try:
                self.stock = value_function(self.ticker_text.get(), self.period_text.get())
                #extract data for yfinance
                tickerDf = self.stock.get_graph() 
                longName = self.stock.get_longname()
            except:
                tk.messagebox.showerror("Required Fields", f"{self.ticker_text.get()}: No data found, symbol may be delisted")
                return

            #plot ticker data using mpf
            mc = mpf.make_marketcolors(up='palegreen', down='red', edge= 'inherit', wick ='black', volume='in')
            s = mpf.make_mpf_style(figcolor = 'midnightblue', facecolor = 'mediumslateblue', rc={'axes.labelcolor':'white','xtick.color':'white', 'ytick.color':'white', 'axes.titlecolor':'white'}, marketcolors = mc, mavcolors = ['black','blue'])
            try:
                fig, ax = mpf.plot(tickerDf, type='candle', mav=(9, 12), returnfig=True, volume=True, figsize=(8,5), style=s, datetime_format='%d-%m-%y')
                fig.suptitle(longName, color='white')
                canvas = FigureCanvasTkAgg(fig, master = self.master)
                canvas.draw()
                #add graph to gui
                canvas.get_tk_widget().grid(row=2, column=0, columnspan=10)
            except:
                tk.messagebox.showerror("Required Fields", f"{self.ticker_text.get()}: No data found, symbol may be delisted")
                return

            #show function buttons
            self.function_label.grid(row=3, column=0, pady=2, sticky=W)
            self.value_btn.grid(row=3, column=1, pady=2, sticky=W)
            self.day_btn.grid(row=3, column=2, pady=2, sticky=W)
            self.port_btn.grid(row=3, column=3, pady=2, sticky=W)

    #main program
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
        
if __name__ == '__main__':
    main()