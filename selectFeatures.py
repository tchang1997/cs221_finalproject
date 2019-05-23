import csv
from sklearn import svm
import numpy as np
import pandas as pd
from sklearn import datasets 
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_decision_regions
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC, SVC
import math
import seaborn as sn

import argparse
import sys

if __name__ == '__main__':
    psr = argparse.ArgumentParser()
    psr.add_argument("-q", "--quiet", help="No plot", action="store_true")
    args = psr.parse_args()

    print("Loading data...")
    colnamesX = ['PPG_y',  'FG%_y', 'APG_y', 'ORPG_y', 'DRPG_y', 'TOPG_y', 'STPG_y', 'BLKPG_y',]
    colnamesY = ['Class']
    PATH_NAME = './csv/final_data.csv'
    bigDF = shuffle(pd.read_csv(PATH_NAME))
    dataX = bigDF[colnamesX]
    dataY = bigDF[colnamesY]
    print("Feature vector table shape:", dataX.shape)
    print("Label table shape:", dataY.shape)

    dataX.to_csv("./csv/data_x.csv")
    dataY.to_csv("./csv/data_y.csv")

    scalerX = StandardScaler()
    newDataX = scalerX.fit_transform(X=dataX.astype('float64'))

    # dividing X, y into train and test data 
    X_train, X_test, y_train, y_test = train_test_split(newDataX, dataY.values.ravel()) 


    print("Training model...")
    # training a linear SVM classifier 
    svm_model_linear = OneVsOneClassifier(LinearSVC(max_iter=100000, C=1.0, ))
    svm_model_linear.fit(X_train, y_train)
    svm_predictions = svm_model_linear.predict(X_test) 

    # model accuracy for X_test   
    accuracy_train = svm_model_linear.score(X_train, y_train) 
    accuracy_test = svm_model_linear.score(X_test, y_test) 
    print("Training accuracy:", accuracy_train)
    print("Test accuracy:", accuracy_test)
    
    # creating a confusion matrix 
    cm = confusion_matrix(y_test, svm_predictions) 
    print("Confusion matrix:\n", cm)

    if args.quiet: sys.exit(0)
    widths = {2 + ix :abs(np.quantile(newDataX[ix], 0.75) - np.quantile(newDataX[ix], 0.25)) / float(2) for ix, col in enumerate(colnamesX[2:])}
    values = {2 + ix : np.median(newDataX[ix]) for ix, col in enumerate(colnamesX[2:])}
    figs, ax = plt.subplots(2, 1, figsize=(6, 8))


    ax[0].set_xlabel(colnamesX[0])
    ax[0].set_ylabel(colnamesX[1])
    print("Plotting main plot...")
    plot_decision_regions(X=np.array(newDataX.astype(np.integer)), 
        y=np.array(dataY['Class'].astype(np.integer)), 
        filler_feature_values=values,
        filler_feature_ranges=widths,
        ax = ax[0],
        clf=svm_model_linear, legend=1)
    print("Plotting confusion matrix...")
    sn.heatmap(cm, annot=True,annot_kws={"size": 10})
    plt.show()







  
  
 
  
