import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn import linear_model
from sklearn import datasets

contests = open('./contestlist.csv')

for contest in csv.reader(contests):
    print(contest[0])
    students = open('./studentlist.csv')
    """
    with open('./'+contest[0]+'/students_data_'+contest[0]+'.csv', 'w') as csv_file:
        fieldnames = ['user_id', 'corr_start', 'corr_prev', 'coef_start', 'intercept_start', 'coef_prev', 'intercept_prev', 'max_score', 'prev_ave', 'prev_std']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()
    """

    total_score = 0
    count = 0
    for student in csv.reader(students):
        data = pd.read_csv('./'+contest[0]+'/'+student[0]+'.csv')
        v_data = pd.read_csv('./../vRoundEd/'+contest[0]+'/'+student[0]+'.csv')
        
        time_from_start = data["past_time_from_start"]
        time_from_prev = data["past_time_from_prev"]
        score =data["score"]

        if student[0] <= 's17t200':
            continue
        
        if max(score) <= 0:
            continue
        correlation_start = np.corrcoef(time_from_start, score)
        correlation_prev = np.corrcoef(time_from_prev, score)
        prev_ave = np.average(time_from_prev)
        std_prev = np.std(time_from_prev)
        
        x_s = data.loc[:, ['past_time_from_start']]
        x_p = data.loc[:, ['past_time_from_prev']]
        y = data.loc[:, ['score']]
        
        clf_s = linear_model.LinearRegression()
        clf_s.fit(x_s, y)
        clf_p = linear_model.LinearRegression()
        clf_p.fit(x_p, y)
        
        users_data =  [student[0], correlation_start[0][1], correlation_prev[0][1], clf_s.coef_[0][0], clf_s.intercept_[0], clf_p.coef_[0][0], clf_p.intercept_[0], max(score), prev_ave, std_prev]
        total_score += max(score)
        count += 1
        if (max(score) < float(contest[6])):
            if(max(time_from_prev) > 60):
                 plt.plot(time_from_start, score, '-o', label=student[0],markersize=1,color='red', linewidth=1.7)
                 print(student[0])
            else:
                 plt.plot(time_from_start, score, '-o', label=student[0],markersize=1,color='blue',linewidth=1.0)
        else:
            plt.plot(time_from_start, score, '-o', label=student[0],markersize=1,color='black', linewidth=0.7)
        """
        data['ds'] = pd.to_datatime(df['submit_time']).dt.date
        model = Prophet()
        
        model.fit(data)
        plt.scatter(time_from_start, score)
        
        future = model.make_future_dataframe(periods,300, freq = 'm')
        forecast = model.predict(future)
        forecast_data.tail(5)
        model.plot(forecast)
        model.plot_components(forecast)
        plt.show()
        """
        
        #print(users_data)
        """
        with open('./'+contest[0]+'/students_data_'+contest[0]+'.csv','a') as add_data:
            writer = csv.writer(add_data)
            writer.writerow(users_data)
        """
        #print('correlation_from_start: ' + str(correlation_start[0][1]))
        #print('correlation_from_prev: ' + str(correlation_prev[0][1])) 
    # print(total_score/count)
    
    plt.xlabel('time')
    plt.ylabel('score')
    plt.xlim(0, 180)
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()
    
#print contests["contest_id"]
