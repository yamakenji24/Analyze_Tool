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

def prediction(df):
    model = Prophet(weekly_seasonality=False, yearly_seasonality=False)
    model.fit(df)
    future = model.make_future_dataframe(periods=6, freq='W')
    forecast = model.predict(future)
    print(forecast['ds'])
    return forecast
    
def each_student(students):
    for student in csv.reader(students):
        df = pd.read_csv('./score/'+student[0]+'.csv', nrows=4)
        student_data = pd.read_csv('./score/'+student[0]+'.csv')
        df['y'] = df['score']
        student_data['ds'] = pd.to_datetime(student_data['ds'], errors='coerce')

        forecast = prediction(df)
        plot_data(forecast, student_data)
    

def plot_data(forecast, actual_data):
    plt.plot(forecast['ds'], forecast['yhat'], '-o', color='blue', label='prediction')
    plt.plot(actual_data['ds'] ,actual_data['score'], '-o', color='red', label='actual data')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()

each_student(students)
