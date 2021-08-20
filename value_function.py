import yfinance as yf
import investpy as investpy
import pandas as pd

#This class is used by the value gui and the main gui to extract data from yfinance and investpy

class value_function:
    def __init__(self, ticker, period):
       #the constructor queries yfinance using inputs from the main gui and creates variables that are used later in the class
        period_dict = {"1 Year":("1y","1d"), 
                        "1 Day":("1d","15m"), 
                        "5 Days":("5d","60m"),
                        "1 Month":("1mo","1d"),
                        "3 Months":("3mo","1d"),
                        "6 Months":("6mo","1d"),
                        "2 Years":("2y","1wk"),
                        "5 Years":("5y","1mo"),
                        "10 Years":("10y","3mo"),
                        "Year to Date":("ytd","1d"),
                        "Maximum":("max","3mo")}
        self.period = period_dict[period][0]
        self.interval = period_dict[period][1]
        self.tick = yf.Ticker(ticker)
        self.bal = self.tick.balance_sheet
        self.earnings = self.tick.earnings
        self.info = self.tick.info
        year_index = []
        #price_hist is created for use of the value screens, consistent period and interval are needed for fair comparisons
        price_hist = self.tick.history(period="5y", interval="1d", actions=False)
        date_list = price_hist.index.tolist()
        for each in date_list:
            year_index.append(each.year)
        self.price_list = price_hist['Close'].tolist()
        d = {'Year':year_index, 'Price':self.price_list}
        df_0 = pd.DataFrame(d)
        self.df = df_0.groupby('Year')['Price'].mean()

    def get_longname(self):
        #used to title main page graph
        return self.info.get("longName")

    def get_graph(self):
        #Second yfinance call of the function, this returns a dataframe for the graph in the main gui
        return self.tick.history(period = self.period, interval=self.interval)

    #The below functions all produce data for purpose of calculating value screens
    def get_EY(self):
        trailing_EPS = self.info.get("trailingEps")
        price = self.info.get("currentPrice")
        return (trailing_EPS/price)

    def get_PE(self):
        #get historic average price
        price = self.df.iloc[-1]
        price_1 = self.df.iloc[-2]
        price_2 = self.df.iloc[-3]
        price_3 = self.df.iloc[-4]

        #get historic number of stocks
        stock = self.bal.iloc[:,0]["Common Stock"]
        stock_1 = self.bal.iloc[:,1]["Common Stock"]
        stock_2 = self.bal.iloc[:,2]["Common Stock"]
        stock_3 = self.bal.iloc[:,3]["Common Stock"]

        #get historic earnings 
        earn = self.earnings["Earnings"].iloc[-1]
        earn_1 = self.earnings["Earnings"].iloc[-2]
        earn_2 = self.earnings["Earnings"].iloc[-3]
        earn_3 = self.earnings["Earnings"].iloc[-4]
      
        #get historic PE
        pe = self.price_earnings(price, earn, stock)
        pe_1 = self.price_earnings(price_1, earn_1, stock_1)
        pe_2 = self.price_earnings(price_2, earn_2, stock_2)
        pe_3 = self.price_earnings(price_3, earn_3, stock_3)

        return pe, pe_1, pe_2, pe_3

    def price_earnings(self, price, earnings, stock):
        eps = (earnings/stock)
        return(price/eps)

    def dividend(self):
        return self.info.get("dividendYield")

    def get_NCAV(self):
        ncav = self.bal.iloc[:,0]["Net Tangible Assets"]
        ncav_per_share = ncav/(self.bal.iloc[:,0]["Common Stock"])
        price = self.df.iloc[-1]
        return ncav_per_share, price

    def get_debt_to_equity(self):
        return self.info.get("debtToEquity")

    def get_current_ratio(self):
        return self.info.get("currentRatio")

    def get_total_debt(self):
        ncav = self.bal.iloc[:,0]["Net Tangible Assets"]
        return ncav, self.info.get("totalDebt")

    def get_average_earnings_growth(self):
        earn = self.earnings["Earnings"].iloc[-1]
        earn_1 = self.earnings["Earnings"].iloc[-2]
        earn_2 = self.earnings["Earnings"].iloc[-3]
        earn_3 = self.earnings["Earnings"].iloc[-4]
        earnings_growth_1 = (earn-earn_1)/earn_1
        earnings_growth_2 = (earn_1-earn_2)/earn_2
        earnings_growth_3 = (earn_2-earn_3)/earn_3
        avg_earnings_growth = (earnings_growth_1 + earnings_growth_2 + earnings_growth_3)/4
        return avg_earnings_growth

    def get_current_price(self):
        return round(self.price_list[-1],1)

    #investpy handles non-stock financial assets better than yfinance, bond and etfs etc
    def ten_year_gilt(self):
        df1 = investpy.bonds.get_bond_information(bond="U.K. 10Y", as_json=False)
        ten_year_gilt = (df1["Prev. Close"][0]/100)
        return ten_year_gilt

    def corporate_bond_yield(self):    
        df1 = investpy.etfs.get_etf_information(etf='Xtrackers USD High Yield Corporate Bond UCITS', country='united kingdom', as_json=False)
        corporate_yield=float((df1["Dividend Yield"][0])[:-1])
        return corporate_yield/100