# LSE-App
Basic Tkinter Application to aid in financial investment decisions, using one main window and three subwindows.
This is purely an excercise in application development and should not be used for actual investment advice.

## Main Window
This window takes the input of a ticker symbol and queeries yfinance to display stock prices over a certain time period.
This window also displays a scrolling stock ticker and buttons linking to the three subwindows.

## Value Window
This window takes stock data from yfinance and bond data from investpy to calculate if said stock satisfies 8 of Benjamin Graham's Value investment screens.
These screens are financial criteria that purportedly indicate if a stock is 'undervalued' at its current price.

 ## Day Window
 This window takes stock price data from yfinance and runs it through a rudimentary Long short-term memory (LSTM) model. The results of this model are then plotted
 against the true values of stock price to demonstrate the accuracy of the model. The model then predicts one day into the future.
 
 ## Portfolio Window
 This window is based upon the idea of an efficent portfolio created by Harry Markowitz. It compares the volatility of stock price movements and then allocates weightings
 to each stock to maximise returns per point of extra volatility, also known as the optimum risky portfolio. This window utilitses a sqlite database to save the portfolio
 stocks and weightings, it displays an efficient frontier graph and four portfolio analysis statistics. 
 
 ## Areas for Improvement
 This is my first endevour into a self-organised project after many tutorials, and as such has many areas for improvement.
 
 -The layout is unintuitive as the prodominant use case of the app (portfolio management) is in a subwindow.
 -The use of Tkinter grately limits the aesthetics of the application, as does my inexperience in UI design.
 -The code is ineffcient and seems to take a long time to perform seemingly simple tasks.
 
 -I plan to reuse some of the functions from this program in the creation of a Flask/Chart.js Dashboard project that will go someway to solving the first two areas for improvement.

