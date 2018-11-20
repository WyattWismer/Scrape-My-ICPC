import plot_wrapper as pw
import data_handler as dh
from user_input import Inputter as Inp
from user_input import Choices as CH
import numpy as np



# Let user select which options they'd like
sm = staticmethod

# From the ranks of a schools teams for a given year choose the points you would like to graph.
CH.rank_point_chooser = sm(Inp.choose_lambda_function(
"choose the points you would like to graph given the ranks of all of a school's teams for a given year"
"select which data points you would like to graph from each year's performance",
"%[0:1] would select only the first point.",
"%[:]"
) or (lambda x: x)) #DEFAULT


CH.trend_point_chooser = sm(Inp.choose_lambda_function(
"select which data point you would like to use in the trend",
"%[-1] would select only the last point.",
"%[0]"
) or (lambda x: x[0])) #DEFAULT



# Load data
dh.load_data(2015,2018)


# Let user choose schools
all_schools = list(dh.data)

default_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']
target_schools = (Inp.choose_options_from_list(all_schools, "school")
or default_schools)





# Plot data
pw.add_target_schools(target_schools)


