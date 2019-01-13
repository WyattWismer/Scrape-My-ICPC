from collections import defaultdict as dd
from scrape import get_standings 
import numpy as np

data = dd(lambda: dd(list))  #school, year, rankings

def load_data(start_year, end_year):
    """
    Loads icpc data in the years spanning the inclusive range from start_year -> end_year
    """
    years = np.arange(start_year, end_year+1)
    for year in years:
        # Get results for a particular year
        standings = get_standings(year)
        assert(standings)

        # Store in data table
        for school in standings:
            data[school][year] = standings[school] 
            data[school][year].sort()


    
