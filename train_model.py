# for data
import csv

# for data management
import csv
import pandas as pd

# for mathematical operations
import numpy as np
import math

# for data preprocessing
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.utils import shuffle

# our model
from sklearn.ensemble import RandomForestClassifier

# for data analysis
from sklearn.metrics import confusion_matrix

# for visualization
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt
import seaborn as sn

# for command line interface
import argparse
import sys

PATH_NAME = './csv/final_data.csv'

class KNNFiller():
    def __init__(self, n, mode):
        self.n = n
        self.mode = mode.lower()
        if mode not in ['mode', 'median', 'mean']:
            raise ValueError("Invalid nearest-neighbor statistic.")

    def fill(self, df):
        pass


if __name__ == '__main__':
    # command line setup
    psr = argparse.ArgumentParser()
    psr.add_argument("-q", "--quiet", help="No plot", action="store_true")
    psr.add_argument("-p", "--path-to-dataframe", help="Path to dataframe", type=str, default=PATH_NAME)
    args = psr.parse_args()


    print("Loading data...")

    #########################################
    #
    #  Feature Selection:
    #  We set colnamesX to the selected features we want. The first two will be graphed.
    #
    ##########################################
    colnamesX = ['APG_y', 'PPG_y', 'RPG_y', 'FG%_y',  'STPG_y', 'BLKPG_y', 'GP_y', 'MPG_y', '2P%_y', '3P%_y']
    colnamesY = ['Class'] # class label

    # read in data
    bigDF = shuffle(pd.read_csv(args.path_to_dataframe)) # shuffle data as we read it in

    # dataFiller = KNNFiller(n=5, mode='median')
    # dataFiller.fill(bigDF)

    dataX = bigDF[colnamesX] # feature data
    dataY = bigDF[colnamesY] # labels
    dataX = dataX.fillna(dataX.median())
    print("Feature vector table shape:", dataX.shape)
    print("Label table shape:", dataY.shape)

    dataX.to_csv("./csv/data_x.csv") 
    dataY.to_csv("./csv/data_y.csv")

    ################################
    #
    # Option one: transform data to a normal distribution. Uncomment these two lines.
    #
    ################################
    ##newDataX = scalerX.fit_transform(X=dataX.astype('float64'))

    ################################
    #
    # Option two: Don't transform the data. This is what this line is.
    #
    ################################
    newDataX = dataX.values

    # dividing X, y into train and test data 
    X_train, X_test, y_train, y_test = train_test_split(newDataX, dataY.values.ravel()) 


    print("Training model...")

    ################################
    #
    # Our actual classifier. Tune these hyperparameters.
    #
    ################################
    clf = RandomForestClassifier(n_estimators=10000, max_features=None, class_weight="balanced")
    clf.fit(X_train, y_train) # learn
    pred = clf.predict(X_test) # predict

    # model accuracy for X_test.  
    accuracy_train = clf.score(X_train, y_train) 
    accuracy_test = clf.score(X_test, y_test) 
    print("Training accuracy:", accuracy_train)
    print("Test accuracy:", accuracy_test)
    print("Params:", clf.get_params())
    
    # creating a confusion matrix. We should have a nice diagonal line.
    cm = confusion_matrix(y_test, pred) 
    print("Confusion matrix:\n", cm)

    if args.quiet: sys.exit(0) # pass in with -q flag to skip graphing

    # These are settings for drawing. Do whatever with these.
    widths = {2 + ix : 20 for ix, col in enumerate(colnamesX[2:])}
    values = {2 + ix : np.median(newDataX[ix]) for ix, col in enumerate(colnamesX[2:])}
    figs, ax = plt.subplots(2, 1, figsize=(6, 8))
    print("Features shown in graph:", colnamesX[:2])
    print("Features flattened in graph:",colnamesX[2:])
    print("Values:", values)
    print("Widths:", widths)
    #figs, ax = plt.subplots(len(colnamesX) + 1, len(colnamesX), figsize=(3, 4))


    ax[0].set_xlabel(colnamesX[0])
    ax[0].set_ylabel(colnamesX[1])
    print("Plotting main plot...")
    figs = plot_decision_regions(X=newDataX, 
        y=np.array(dataY['Class'].astype(np.integer)), 
        filler_feature_values=values,
        filler_feature_ranges=widths,
        clf=clf, legend=2, ax=ax[0])
    print("Plotting confusion matrix...")
    sn.heatmap(cm, annot=True,annot_kws={"size": 10})
    plt.show()







  
  
 
  