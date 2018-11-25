import plot_wrapper as pw
import data_handler as dh
from user_input import Inputter as Inp
from user_input import Choices as CH
import numpy as np




# From the ranks of a schools teams for a given year choose the points you would like to graph.
CH.add_choice(
'rank_point_chooser',
Inp.choose_lambda_function,
flavor=("choose the points you would like to graph given the "
"ranks of all of a school's teams for a given year"),
example="%[0:1] would select only the first point.",
default="%[:]"             
)

# Select which data points you would like to use from a schools performance for a particular year
CH.add_choice(
'trend_point_chooser',
Inp.choose_lambda_function,
flavor="select which data point you would like to use in the trend",
example="%[-1] would select only the last point.",
default="%[0]"
)



# Load data
dh.load_data(2015,2018)


# Let user choose schools
all_schools = list(dh.data)

default_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']
target_schools = (Inp.choose_options_from_list(all_schools, "school")
or default_schools)





# Plot data
pw.add_target_schools(target_schools)


