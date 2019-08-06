import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

contests = open('./vrounded_contest.csv')

for contest in csv.reader(contests):
    #students = open('./studentlist.csv')
    students = open('../tProgrEss/'+contest[10]+'/students_data_'+contest[10]+'.csv')
    """
    with open('./'+contest[10]+'/times_raised.csv', 'w') as csv_file:
        fieldnames = ['user_id', 'times_raised']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()
    """
    
    print(contest[10])
    for student in csv.reader(students):
        if student[0] == 'user_id':
            continue
        
        data = pd.read_csv('./'+contest[10]+'/'+student[0]+'.csv')
        tpro_data = pd.read_csv('../tProgrEss/'+contest[10]+'/'+student[0]+'.csv')
        
        raised_time = data['time_from_start']
        count = data['times_raised']
        score = tpro_data['score']
        mode = data['mode']
        
        if count.empty:
            continue
        else:
            if max(raised_time) > 180:
                continue
            times = max(count)

        flag = False
        discover = np.array([])
        
        student_data = open('./'+contest[10]+'/'+student[0]+'.csv')
        for each_data in csv.reader(student_data):
            
            if each_data[3] == '10':
                flag = True
            elif each_data[3] == '50':
                if flag == False:
                    discover = np.append(discover, each_data[0])
                    flag = True
            elif each_data[3] == '100':
                flag = False
        if len(discover) != 0:
            print(student[0], discover)
        users_data = ([student[0], times])
       # plt.plot(raised_time, mode, '-o', label=student[0])
        """
        with open('./'+contest[10]+'/times_raised.csv', 'a') as add_data:
            writer = csv.writer(add_data)
            writer.writerow(users_data)
        """
    """   
    plt.xlabel('time')
    plt.ylabel('mode')
    plt.xlim(0, 180)
    plt.grid()
    plt.legend()
    plt.show()
    """
