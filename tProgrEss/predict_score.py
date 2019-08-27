import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.offline as py
import csv
from datetime import datetime
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

students = open('./studentlist.csv')
contests = open('./contestlist.csv')

#for student in csv.reader(students):

df = pd.read_csv('./score/s17t285.csv', nrows=4)
data = pd.read_csv('./score/s17t285.csv')
#df = pd.read_csv('./W01_C01/s16t229.csv')

#df['ds'] = df[df['past_time_from_start'] < 90].submit_time
#df['y'] = df[df['past_time_from_start'] < 90].score
df['y'] = df['score']
data['yhat'] = data['score']
data['yhat_lower'] = data['score']
data['yhat_upper'] = data['score']
data['ds'] = pd.to_datetime(data['ds'], errors='coerce')
#data.plot()
#xfmt = mdates.DateFormatter("%y/%m/%d")
#data.xaxis.set_major_formatter(xfmt)

#print(df['ds'])

model = Prophet(weekly_seasonality=False, yearly_seasonality=False)
model.fit(df)

future = model.make_future_dataframe(periods=6, freq='W')
forecast = model.predict(future)
print(forecast)
fig = model.plot(forecast)
model.plot(data)
#model.plot(data['ds'], data['score'])
plt.show()
