from matplotlib import figure, lines
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
from tensorflow.python.ops.gen_dataset_ops import prefetch_dataset
import yfinance as yf
import mplfinance as mpf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import datetime

#this class creates a simple LTSM model using tensor flow and sklearn, this model uses linear time series
#stock price data from the last decade to predict the last 60 days of prices, these prices are then plotted
#against the real stock prices to judge accuracy. It also predicts one day into the future.
#Area for improvement, this model is based on an online course and is not optimised for stock price prediction.

class day_function:
    
    def get_tommorrow(ticker):

        #get relatent datetime
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        ten_years_date = (datetime.datetime.now() - datetime.timedelta(days=10*365)).strftime('%Y-%m-%d')
        two_years_date = (datetime.datetime.now() - datetime.timedelta(days=2*365)).strftime('%Y-%m-%d')
        two_years_date_minus = (datetime.datetime.now() - datetime.timedelta(days=((2*365)-1))).strftime('%Y-%m-%d')

        company = ticker
        ticker = yf.Ticker(company)
        data = ticker.history(start=ten_years_date, end=two_years_date, interval="1d")

        #prepare data 
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

        prediction_days = 60

        x_train = []
        y_train = []

        #fill X list with 60 days previous prices, and Y with the 'current' price
        for x in range(prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x-prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])

        #reshape x&y training data
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        #build model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train,y_train, epochs=5, batch_size=32)

        ### test the model accuracy of exitsting data ###
        #Load Test data

        test_data = ticker.history(start=two_years_date_minus, end=current_date, interval="1d")
        actual_prices = test_data['Close'].values
        #add real values to earlier extracted data
        total_dataset = pd.concat((data['Close'], test_data['Close']))

        model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
        model_inputs = model_inputs.reshape(-1,1)
        model_inputs = scaler.transform(model_inputs)

        # Make predictions

        x_test = []

        for x in range(prediction_days, len(model_inputs)):
            x_test.append(model_inputs[x-prediction_days:x, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predicted_prices = model.predict(x_test)
        predicted_prices = scaler.inverse_transform(predicted_prices)
        predicted_prices = np.array(predicted_prices)
        predicted_prices = np.squeeze(predicted_prices)

        predicted_dataframe = test_data
        actual_dataframe = test_data

        #mpl finance (mpf) only takes dataframe with columns of [Open, Close, High, Low]
        #the below fills a dataframe of that shape with predicted and actual prices
        predicted_dataframe['Open'] = predicted_prices
        predicted_dataframe['Close'] = predicted_prices
        predicted_dataframe['High'] = predicted_prices
        predicted_dataframe['Low'] = predicted_prices
        
        actual_dataframe['Open'] = actual_prices
        actual_dataframe['Close'] = actual_prices
        actual_dataframe['High'] = actual_prices
        actual_dataframe['Low'] = actual_prices

        #graph miscellaneous data
        legend_tuple = f"Real {company} Price", f"Predicted {company} Price"
        path_to_figure = "daytrade.png"
    
        #plot and save graph
        s = mpf.make_mpf_style(figcolor = 'midnightblue', facecolor = 'mediumslateblue', rc={'axes.labelcolor':'white','xtick.color':'white', 'ytick.color':'white', 'axes.titlecolor':'white'})
        ap = [mpf.make_addplot(predicted_prices, type='line', color='black')]
        fig, ax = mpf.plot(actual_dataframe, type='line', returnfig=True, figsize=(8,5), linecolor="palegreen", style=s, addplot=ap, datetime_format='%d-%m-%y')
        ax[0].legend(legend_tuple)
        fig.savefig(path_to_figure)

        #predict next day
        real_data = [model_inputs[len(model_inputs)+1 - prediction_days:len(model_inputs+1), 0]]
        real_data = np.array(real_data)
        real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1],1))

        prediction = model.predict(real_data)
        prediction = scaler.inverse_transform(prediction)

        return prediction
