import plot_wrapper as pw
import data_handler as dh
from user_input import Inputter as Inp
from user_input import Choices as CH
import numpy as np


target_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']

# Let user select which options they'd like
sm = staticmethod

CH.point_chooser = sm(Inp.get_lambda_function(
"select which data points you'd like",
"[%[0]] would select only the first point"
) or (lambda x: x)) #DEFAULT



# Load data
dh.load_data(2015,2018)

# Plot data
pw.add_target_schools(target_schools)


