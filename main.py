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



#max_offset = 0.15
#offset = 0 if len(target_schools)==1 else max_offset/(len(target_schools)-1)

# Load data
dh.load_data(2015,2018)

# Plot data
pw.start()
for school in target_schools:
    pw.add_school(school)
pw.end()


