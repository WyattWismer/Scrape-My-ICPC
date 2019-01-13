import matplotlib.pyplot as plt
from math import ceil
import numpy as np
from user_input import Choices as CH

from data_handler import data


# STATE 
color_ind = {}
schools = None 
local_func = None

# CONSTANT
MAX_OFFSET=0.25
      
# LOCAL FUNCTIONS
class LF:
    """
    Exposes functions loaded in from choices configuration
    """
    def __init__(self, functions):
        self.func = functions 
    def __getitem__(self, key):
        assert(key in self.func) 
        return self.func[key]

def get_color(school):
    """
    Generates the color for a particular school
    """
    global color_ind
    cmap = plt.get_cmap('tab10')
    if school not in color_ind:
        color_ind[school] = len(color_ind)
    return cmap(color_ind[school])

def add_school(sid):
    """
    Plot results for a school with a given school id
    """
    # plot results for school
    plot_all_results(sid)    

    # plot trend
    plot_trend(sid)

def get_offset(ind): 
    """
    Get offset used in plotting year result
    """
    n = len(schools)
    if(n==1): return 0
    step = MAX_OFFSET/(n-1)
    return ind*step - MAX_OFFSET/2

def plot_year_result(school, year, offset, has_legend):
    """
    Plots vertical line to display rankings for a given year 
    """
    c = get_color(school)

    # get rankings
    rankings = data[school][year]
    # apply users point chooser
    rankings = local_func['rank_point_chooser'](rankings)

    n = len(rankings)
    x = np.full(n, year+offset)
    
    line_label = (has_legend and school) or None
    line, = plt.plot(x, rankings, marker='o', color=c, label=line_label)


def plot_all_results(sid):
    """
    Plots year results across all years for a given school
    """
    tot_offset = get_offset(sid) 
    school = schools[sid]
    school_data = (e for e in sorted(data[school]))

    plot_year_result(school, next(school_data), tot_offset, True)

    for year in school_data:
        plot_year_result(school, year, tot_offset, False)


def plot_trend(school):
    """
    Plots trend line for a particular school
    """
    for sid, school in enumerate(schools):
        c = get_color(school)
        school_data = sorted(data[school])

        y = []
        for year in school_data:
            rankings = data[school][year]
            ranking = local_func['trend_point_chooser'](rankings)
            assert(type(ranking)==int)
            y.append(ranking)

        x = np.array(school_data) + get_offset(sid)
        y = np.array(y)
        plt.plot(x,y,color=c)


def setup():
    """
    Boilerplate for matplotlib.
    Populates local functions class.
    """
    plt.figure()
    assert(CH.func)
    global local_func
    local_func = LF(CH.func)

def finalize():
    """
    More Boilerplate for matplotlib! 
    Sets graph boundaries, axis step and labels.
    Displays graph.
    """
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


def add_target_schools(target_schools):
    """
    Adds given schools & displays graph
    """
    global schools
    schools = target_schools
    assert(schools) 

    setup()

    n = len(schools)
    for sid in range(n):
        add_school(sid)

    finalize()





