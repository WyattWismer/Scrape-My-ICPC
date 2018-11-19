import matplotlib.pyplot as plt
from math import ceil
import numpy as np

from data_handler import data

# FLAGS
#MAX_OFFSET=0.1

# STATE 
color_ind = {}
schools = []


      


def get_color(school):
    global color_ind
    cmap = plt.get_cmap('tab10')
    if school not in color_ind:
        color_ind[school] = len(color_ind)
    return cmap(color_ind[school])

def add_school(school):
    # add school to list
    schools.append(school)

    # plot results for school
    plot_all_results(school)    

    # plot trend
    plot_trend(school)
    
def plot_year_result(school, year, offset, has_legend):
    """
    Plots a vertical line showing rankings for a given year 
    """
    c = get_color(school)

    rankings = data[school][year]
    n = len(rankings)
    x = np.full(n, year+offset)

    line, = plt.plot(x, rankings, marker='o', color=c)
    line.has_legend = has_legend 

def get_offset(): #TODO
    return 0.1

def plot_all_results(school):
    assert(schools)

    tot_offset = get_offset()*(len(schools)-1) 
    school_data = data[school]
    has_legend = (school==schools[0])

    for year in sorted(school_data):
        plot_year_result(school, year, tot_offset, has_legend)

def build_legend(): #TODO
    pass

def plot_trend(school): #TODO
    pass


def start():
    plt.figure()


  
def end():
    up_to_int = lambda x: int(ceil(x))
    x_min, x_max = map(up_to_int, plt.xlim())
    y_min, y_max = map(up_to_int, plt.ylim())
    y_min = max(y_min,1)

    plt.xticks(np.arange(x_min,x_max,1))
    plt.yticks(np.arange(y_min,y_max,3))

    title_font = {'weight' : 'bold',
                  'size'   : 20} 

    plt.title("ICPC ECNA Regional Comparison", **title_font)
    plt.xlabel("Year")
    plt.ylabel("Rank")

    plt.show()
            







