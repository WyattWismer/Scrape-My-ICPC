import plot_wrapper as pw
import data_handler as dh
from user_input import Inputter as Inp
from user_input import Choices as CH
import numpy as np


target_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']

# Let user select which options they'd like
sm = staticmethod

CH.rank_point_chooser = sm(Inp.get_lambda_function(
"select which data points you would like to graph from each year's performance",
"%[0:1] would select only the first point.",
"%[:]"
) or (lambda x: x)) #DEFAULT


CH.trend_point_chooser = sm(Inp.get_lambda_function(
"select which data point you would like to use in the trend",
"%[-1] would select only the last point.",
"%[0]"
) or (lambda x: x[0])) #DEFAULT


# Load data
dh.load_data(2015,2018)

# Plot data
pw.add_target_schools(target_schools)


