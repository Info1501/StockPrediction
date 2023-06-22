#Import necessary lib
import datetime
import math
import pandas_datareader as web
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM,Dense
import streamlit as st
import plotly.graph_objects as go
class LSTModel:

	def split_sequence(sequence, n_steps):
		X, y = list(), list()
		for i in range(len(sequence)):
			# find the end of this pattern
			end_ix = i + n_steps
			# check if we are beyond the sequence
			if end_ix > len(sequence)-1:
				break
			# gather input and output parts of the pattern
			seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
			X.append(seq_x)
			y.append(seq_y)
		return np.array(X), np.array(y)

	def BuildModel_Test(self):


		plt.style.use('fivethirtyeight')
		#Gather data
		df = web.DataReader('AAPL', data_source='stooq', start='2012-01-01', end=datetime.date.today())
		# Extract needed data and convert
		data = df.filter(['Close'])
		data = data.iloc[::-1]
		dataset = data.values

		# Prepare data for training
		train_len = math.ceil(len(dataset) * .8)
		scaler = MinMaxScaler(feature_range=(0, 1))
		scaled_data = scaler.fit_transform(dataset)
		train_data = scaled_data[0:train_len, :]

		x_train = []
		y_train = []
		for i in range(60, len(train_data)):
			x_train.append(train_data[i - 60:i, 0])
			y_train.append(train_data[i, 0])

		x_train, y_train = np.array(x_train), np.array(y_train)
		x_train=np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

		#Build model

		model = Sequential()
		model.add(LSTM(50,return_sequences=True,input_shape=(x_train.shape[1],1)))
		model.add(LSTM(50,return_sequences=False))
		model.add(Dense(25))
		model.add(Dense(1))
		model.compile(optimizer="adam",loss="mean_squared_error")
		model.fit(x_train,y_train,batch_size=1,epochs=1)

		#Testing data

		test_data = scaled_data[train_len-60:, :]
		x_test = []
		y_test = dataset[train_len:,:]
		for i in range(60,len(test_data)):
			x_test.append(test_data[i-60:i,0])
		x_test = np.array(x_test)
		x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

		#Predicting
		predictions = model.predict(x_test)
		predictions = scaler.inverse_transform(predictions)

		rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))

		#Plot test
		train = data[:train_len]
		valid = data[train_len:]
		valid["Predictions"] = predictions
		print(predictions)
		plt.figure(figsize=(16,8))
		plt.title("Demo Model Apple Stock")
		plt.xlabel("Date",fontsize=18)
		plt.ylabel("Closing Price",fontsize=18)
		plt.plot(train["Close"])
		plt.plot(valid[["Close","Predictions"]])
		plt.legend(["Train","Val","Prediction"], loc = "lower right")
		#plt.show()
		st.pyplot(plt)



	def BuildModel_Real(self,Stock):

		try:
			# Gather data
			end = datetime.date.today()
			start = end - datetime.timedelta(days=360)
			df = web.DataReader(Stock, 'stooq', start, end)

			# Extract needed data and convert
			data = df.filter(['Close'])
			data = data.iloc[::-1]
			dataset = data.values
			scaler = MinMaxScaler(feature_range=(0, 1))
			scaled_dataset = scaler.fit_transform(dataset)

			# Test Data
			x_train = []
			y_train = []
			for i in range(30, len(scaled_dataset)):
				x_train.append(scaled_dataset[i - 30:i, 0])
				y_train.append(scaled_dataset[i, 0])

			x_train, y_train = np.array(x_train), np.array(y_train)
			x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

			# Build model
			model = Sequential()
			model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
			model.add(LSTM(50, return_sequences=False))
			model.add(Dense(25))
			model.add(Dense(1))
			model.compile(optimizer="adam", loss="mean_squared_error")
			model.fit(x_train, y_train, batch_size=1, epochs=10)

			# Predicting next day based on the last month
			data = df.filter(['Close'])
			data = data.iloc[::-1]
			data_predict = data[-30:].values
			data_predict_scaled = scaler.fit_transform(data_predict)

			x_predict_test = []
			x_predict_test.append(data_predict_scaled)
			x_predict_test = np.array(x_predict_test)
			x_predict_test = np.reshape(x_predict_test, (x_predict_test.shape[0], x_predict_test.shape[1], 1))

			predicted_price = model.predict(x_predict_test)
			predicted_price = scaler.inverse_transform(predicted_price)

			# Plot test using Plotly
			predicted_date = datetime.date.today() + datetime.timedelta(1)

			fig = go.Figure()
			fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Values"))
			fig.add_trace(go.Scatter(x=[predicted_date], y=predicted_price[0], mode='markers', name="Prediction",
									 marker=dict(color="red")))

			fig.update_layout(title="Prediction", xaxis_title="Date", yaxis_title="Closing")

			st.plotly_chart(fig)
			st.write("### Exact closing price prediction: " + str(predicted_price).replace("[", "").replace("]", ""))
		except:
			st.write("### There is no such stock ticker !!")






