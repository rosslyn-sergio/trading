import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PlotModel(object):
        def __init__(self, title, xlabel, ylabel):
                self.title = title
                self.xlabel = xlabel
                self.ylabel = ylabel

def create_training_set(filename):
	#read csv
	df = pd.read_csv(filename, index_col="Date", parse_dates=True, na_values=['nan'])
	
	#normalise
	df = df/df.iloc[0,:]
	
	#add daily returns
	df["Daily_Returns"] = (df["Adj Close"] / df["Adj Close"].shift(1)) - 1
	df.at[df.index.values[0], ["Daily_Returns"]] = 0

	#calculate statistics
	stats_df = pd.DataFrame(index=pd.DatetimeIndex([]))
	#rolling average
	windows = [5,10]
	for w in windows:
		#rolling mean	
		temp_df = get_rolling_mean(df, w)
		stats_df = pd.concat([stats_df, temp_df], axis=1, join='outer' if w == windows[0] else 'inner')
		
		#rolling std
		temp_df = get_rolling_standard_deviation(df, w)
		stats_df = pd.concat([stats_df, temp_df], axis=1, join='outer' if w == windows[0] else 'inner')
		
		#rolling high
		temp_df = get_rolling_high(df, w)
		stats_df = pd.concat([stats_df, temp_df], axis=1, join='outer' if w == windows[0] else 'inner')
		
		#rolling low
		temp_df = get_rolling_low(df, w)
		stats_df = pd.concat([stats_df, temp_df], axis=1, join='outer' if w == windows[0] else 'inner')


	#Add labels
	df["Label"] = (df["Adj Close"] < df["Adj Close"].shift(-1)).astype(int)
	label5 = []
	for i in range(len(df)):
		label5.append(get_peak_label(df, 5, i))
	df["Label5"] = label5
	return df, stats_df

def get_peak_label(df, window, index):
	current = df["Adj Close"].iloc[index]
	prev_max = df["Adj Close"].iloc[index:index+window].max()
	prev_min = df["Adj Close"].iloc[index:index+window].min()
	next_max = df["Adj Close"].iloc[index-window:index].max()
	next_min = df["Adj Close"].iloc[index-window:index].min()
	if current ==  72.029999:
		print(index,current, prev_max, prev_min, next_max, next_min)
	if current >= prev_max and current >= next_max:
		print(2)
		return 2
	if current <= prev_min and current <= next_min:
		return 0
	return 1
 
def calculate_statistics(df):
	pass

def get_rolling_mean(df, window=20):
	res_df = df[["Adj Close","Daily_Returns"]].rolling(center=False,window=window).mean()
	res_df.columns = ["Adj_Close_Mean{}".format(window),"Daily_Returns_Mean{}".format(window)]
	return res_df


def get_rolling_standard_deviation(df,window=20):
	res_df = df[["Adj Close", "Daily_Returns"]].rolling(center=False, window=window).std()
	res_df.columns = ["Adj_Close_Std{}".format(window),"Daily_Returns_Std{}".format(window)]
	return res_df

def get_rolling_high(df, window=20):
	res_df = df[["High"]].rolling(center=False, window=window).max()
	res_df.columns = ["High{}".format(window)]
	return res_df

def get_rolling_low(df, window=20):
	res_df = df[["Low"]].rolling(center=False, window=window).min()
	res_df.columns = ["Low{}".format(window)]
	return res_df

def plot_data(df, col):
        df[col].plot()
        plt.show()

def plot_logistic_regression_data(df, xcol, ycol, feature, plotModel):
        df_possitive = df[df[feature] == 1]
        df_negative = df[df[feature] == 0]
        plt.plot(df_possitive[xcol], df_possitive[ycol], 'go', df_negative[xcol], df_negative[ycol], 'rx')
        plt.title(plotModel.title)
        plt.xlabel(plotModel.xlabel)
        plt.ylabel(plotModel.ylabel)
        plt.show()

def plot_ternary_log_reg_data(df, xcol, ycol, feature, plotModel):
	df_possitive = df[df[feature] == 2]
	df_negative = df[df[feature] == 0]
	df_neutral = df[df[feature] == 1]
#	plt.plot(df_possitive[xcol], df_possitive[ycol], 'go', df_negative[xcol], df_negative[ycol], 'ro', df_neutral[xcol], df_neutral[ycol], 'bo')
	plt.plot(df_possitive[xcol], df_possitive[ycol], 'go', df_negative[xcol], df_negative[ycol], 'ro')
	plt.title(plotModel.title)
	plt.xlabel(plotModel.xlabel)
	plt.ylabel(plotModel.ylabel)
	plt.show()

def normalise(df, columns):
        for c in columns:
                df[[c]] = (df[[c]] - df[[c]].mean()) / df[[c]].std()

