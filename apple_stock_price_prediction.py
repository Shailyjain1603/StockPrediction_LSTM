# -*- coding: utf-8 -*-
"""Apple_Stock_Price_Prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dxYzTvLviK0CjzjhsKLRszHwJU5_W8rr
"""

# Description: This program uses an artificial recurrent neural network called Long Short Term Memory(LSTM)
#              to predict the closing stock price of a corporation (Apple Inc.) using the past 60 day stock price.

# Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Get the stock quote
import yfinance as yf
df = yf.download('AAPL', start='2012-01-01', end='2019-12-18')

# Show the data
df

# get the number of rows and columns
df.shape

#visualise the closing price history
plt.figure(figsize=(16,8))
plt.title('Closing Price History')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price ', fontsize=18)
plt.show()

#Create a new dataframe with only the "Close Column"
data= df.filter(['Close'])
#convert the datset into an nump array
dataset= data.values
# get the number of rows to train the model on
training_data_len= math.ceil( len(dataset) * .8)
training_data_len

#scale the data
scaler= MinMaxScaler(feature_range=(0,1))
scaled_data= scaler.fit_transform(dataset)

scaled_data

#create the training dataset
# Create the scaled training dataset
train_data= scaled_data[0:training_data_len,:]
#Split the data into x_train and y_train data sets
x_train=[]
y_train=[]

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i,0])
  if i<=60:
    print(x_train)
    print(y_train)
    print()

#Convert the x_train and y_train to numpy arrays
x_train, y_train= np.array(x_train), np.array(y_train)

#Reshape the data
x_train= np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
x_train.shape

#Build the LSTM model
model= Sequential()
model.add(LSTM(50, return_sequences= True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(50, return_sequences= False ))
model.add(Dense(25))
model.add(Dense(1))

# compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

#Train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)

#Create the testing dataset
#Create a new aray containing scaled values from index 1543 to 2003
test_data= scaled_data[training_data_len-60: ,:]
#create the data sets x_test and y_test
x_test=[]
y_test=dataset[training_data_len: ,:]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])

# convert the data into a numpy array
x_test= np.array(x_test)

#Reshape the data
x_test= np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

#Get the models predicted price values
predictions= model.predict(x_test)
predictions=scaler.inverse_transform(predictions)

#Get the root mean squared error(RMSE)
rmse= np.sqrt( np.mean(predictions- y_test)**2)
rmse

#Plot the data
train= data[:training_data_len]
valid= data[training_data_len:]
valid['Predictions']= predictions
#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price ', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train','Val', 'Predictions'], loc='lower right')
plt.show()

#Show the valid and predicted prices
valid

#Get the quote
apple_quote= yf.download('AAPL', start='2012-01-01', end='2019-12-18')
#Create a new data frame
new_df= apple_quote.filter(['Close'])
# get the last 60 day closing price values ad convert the dataframe into an
last_60_days = new_df[-60:].values
#scale the data
last_60_days_scaled=scaler.transform(last_60_days)
#create an empty list
X_test=[]
# Append the past 60 days
X_test.append(last_60_days_scaled)
#Convert the X_test data set into a numpy array
X_test= np.array(X_test)
#reshape the data
X_test=np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
#Get the predicted scaled price
pred_price= model.predict(X_test)
#undo teh scaling
pred_price= scaler.inverse_transform(pred_price)
print(pred_price)

apple_quote2= yf.download('AAPL', start='2019-12-18', end='2019-12-19')
print(apple_quote2['Close'])