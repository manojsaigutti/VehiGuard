
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.cm import rainbow

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets, linear_model
from sklearn.metrics import accuracy_score, make_scorer

def takeInput():
    inputValues = ['2.0','2.0','-2.2','-2.2']    
    print("\n") 
    final_Result = knn_classifier.predict([inputValues])
    final_Result = svc_clf.predict([inputValues])
    print(final_Result)
    
    if final_Result[0] == 1:
        print('NORMAL CONDITION')
    elif final_Result[0] == 2:
        print('AVERAGE  CONDITION')
    elif final_Result[0] == 3:
        print('SEVERE CONDITION')
    else: 
        print('GOOD condition')     
        
        
accdt = pd.read_csv("jai.csv")
y = accdt['RES']
X = accdt.drop(['RES'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 0)
knn_classifier = KNeighborsClassifier(n_neighbors = 4)
knn_classifier.fit(X_train, y_train)

knn_preds = knn_classifier.predict(X_test)
knn_acc = accuracy_score(y_test, knn_preds)
print("Accuracy with KNN: ", accuracy_score(y_test, knn_preds))


svc_clf = SVC(gamma='scale')
svc_clf.fit(X_train,y_train)
svc_preds = svc_clf.predict(X_test)
svc_acc = accuracy_score(y_test, svc_preds)
print("Accuracy with SVC: ", accuracy_score(y_test, svc_preds))

regr = LogisticRegression(solver="liblinear").fit(X_train,y_train)
regr_preds = regr.predict(X_test)
regr_acc = accuracy_score(y_test, regr_preds)
print("Accuracy with LR: ", accuracy_score(y_test, svc_preds))

takeInput()

 
