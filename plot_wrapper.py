import matplotlib.pyplot as plt
from math import ceil
import numpy as np
from user_input import Choices as CH

from data_handler import data


# STATE 
color_ind = {}
schools = None 

# CONSTANT
MAX_OFFSET=0.25


      


def get_color(school):
    global color_ind
    cmap = plt.get_cmap('tab10')
    if school not in color_ind:
        color_ind[school] = len(color_ind)
    return cmap(color_ind[school])

def add_school(sid):
    # plot results for school
    plot_all_results(sid)    

    # plot trend
    plot_trend(sid)

def add_target_schools(target_schools):
    global schools
    start()

    schools = target_schools
    n = len(schools)
    assert(n>0)

    for sid in range(n):
        add_school(sid)

    end()

    
def plot_year_result(school, year, offset, has_legend):
    """
    Plots a vertical line showing rankings for a given year 
    """
    c = get_color(school)

    # get rankings
    rankings = data[school][year]
    # apply users point chooser
    rankings = CH.rank_point_chooser(rankings)

    n = len(rankings)
    x = np.full(n, year+offset)
    
    line_label = (has_legend and school) or None
    line, = plt.plot(x, rankings, marker='o', color=c, label=line_label)

def get_offset(ind): 
    n = len(schools)
    if(n==1): return 0
    step = MAX_OFFSET/(n-1)
    return ind*step - MAX_OFFSET/2

def plot_all_results(sid):
    tot_offset = get_offset(sid) 
    school = schools[sid]
    school_data = (e for e in sorted(data[school]))

    plot_year_result(school, next(school_data), tot_offset, True)

    for year in school_data:
        plot_year_result(school, year, tot_offset, False)


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

    plt.legend()
    plt.title("ICPC ECNA Regional Comparison", **title_font)
    plt.xlabel("Year")
    plt.ylabel("Rank")

    plt.show()
            







