import plot_wrapper as pw
import data_handler as dh
import numpy as np


target_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']

#max_offset = 0.15
#offset = 0 if len(target_schools)==1 else max_offset/(len(target_schools)-1)

# Load data
dh.load_data(2015,2018)

# Plot data
pw.start()
for school in target_schools:
    pw.add_school(school)
pw.end()


