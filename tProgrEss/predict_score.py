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
def predict_each_contests(df):
    model = Prophet(
        weekly_seasonality=False,
        yearly_seasonality=False,
        changepoint_prior_scale=0.01
    )
    model.fit(df)
    future = model.make_future_dataframe(periods=100, freq='min')
    forecast = model.predict(future)
    print(forecast)
    return forecast
    
def each_contests(student):
    contests = open('./contestlist.csv')
    for contest in csv.reader(contests):
        data = pd.read_csv('./'+contest[0]+'/'+student[0]+'.csv')
        if len(data) <= 1:
            continue
        print(data)
        data['ds'] = pd.to_datetime(data['submit_time'])
        data['y'] = data['score']
        data2 = data.copy()
        data2['ds'] = pd.to_datetime(data2['ds'])
        if len(data2['past_time_from_start'] < 90):
            data2 = data2[data2['past_time_from_start'] < 120]
        else:
            data2 = data2[data2['past_time_from_start'] < 90]
        forecast = predict_each_contests(data2)
        plot_data(forecast, data, student, contest)
        
def each_student(students):
    for student in csv.reader(students):
        each_contests(student)
        """
        df = pd.read_csv('./score/'+student[0]+'.csv', nrows=4)
        student_data = pd.read_csv('./score/'+student[0]+'.csv')
        df['y'] = df['score']
        student_data['ds'] = pd.to_datetime(student_data['ds'], errors='coerce')

        forecast = prediction(df)
        plot_data(forecast, student_data)
        """

def plot_data(forecast, actual_data, student, contest):
    plt.clf()
    plt.plot(forecast['ds'], forecast['yhat'], '-o', color='blue', label='prediction')
    plt.plot(actual_data['ds'] ,actual_data['score'], '-o', color='red', label='actual data')
    plt.legend(loc='upper left')
    plt.ylim(0, 1000)
    plt.title(contest[0]+': '+student[0])
    plt.grid()
    plt.savefig('./prediction/'+student[0]+'/'+contest[0]+'.png')
    plt.pause(.01)
    
def debug():
    for contest in csv.reader(contests):
        data = pd.read_csv('./'+contest[0]+'/s16t266.csv')
        data['ds'] = pd.to_datetime(data['submit_time'])
        data['y'] = data['score']
        forecast = predict_each_contests(data)
#debug()
each_student(students)
