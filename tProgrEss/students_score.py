import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn import linear_model
from sklearn import datasets

students = open('./studentlist.csv')

for student in csv.reader(students):
    contests = open('./contestlist.csv')
    total_score = 0

    with open('./score/'+student[0]+'.csv', 'w') as csv_file:
        fieldnames = ['contest', 'ds', 'score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
    for contest in csv.reader(contests):
        data = pd.read_csv('./'+contest[0]+'/'+student[0]+'.csv')
        
        score = data["score"]
        total_score += max(score)
        user_score = [contest[0], contest[7], total_score]
        
        with open('./score/'+student[0]+'.csv', 'a') as add_data:
            writer = csv.writer(add_data)
            writer.writerow(user_score)
        
