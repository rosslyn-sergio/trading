import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PlotModel(object):
        def __init__(self, title, xlabel, ylabel):
                self.title = title
                self.xlabel = xlabel
                self.ylabel = ylabel

def read_csv_data(filename):
        df = pd.read_csv(filename, header=None, delimiter=",", dtype=np.float64)
        return df

def plot_data(df, xcol, ycol):
        plt.plot(df[xcol], df[ycol], "rx")
        plt.show()

def plot_logistic_regression_data(df, xcol, ycol, feature, plotModel):
        df_possitive = df[df[feature] == 1]
        df_negative = df[df[feature] == 0]
        plt.plot(df_possitive[xcol], df_possitive[ycol], 'go', df_negative[xcol], df_negative[ycol], 'rx')
        plt.title(plotModel.title)
        plt.xlabel(plotModel.xlabel)
        plt.ylabel(plotModel.ylabel)
        plt.show()

def normalise(df, columns):
        for c in columns:
                df[[c]] = (df[[c]] - df[[c]].mean()) / df[[c]].std()

