from collections import defaultdict as dd
from scrape import get_standings 
import numpy as np

data = dd(lambda: dd(list))  #school, year, rankings

def load_data(start_year, end_year):
    years = np.arange(start_year, end_year+1)
    for year in years:
        standings = get_standings(year)
        assert(standings)

        for school in standings:
            data[school][year] = standings[school] 
            data[school][year].sort()


    
