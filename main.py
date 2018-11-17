from scrape import get_standings as gs
from helper import min_max

from collections import defaultdict as dd

import matplotlib.pyplot as plt
from matplotlib import container
import numpy as np


data = dd(lambda: dd(list))  #school, year, ranking


start_year, end_year = 2015, 2018
years = np.arange(start_year, end_year+1)

for year in years:
    standings = gs(year)
    for school in standings:
        data[school][year] = standings[school] 

#print ','.join(map(lambda s: "'"+s+"'",list(data)))

#target_schools = ['University of Dayton','Brock University','Eastern Michigan University','Purdue University','McMaster University','University of Notre Dame','Wright State University','Indiana University Bloomington','Indiana State University','Xavier University','Carnegie Mellon University','Hope College','University of Waterloo','Grove City College','Ohio State University','Edinboro University','University of Toledo','Miami University','Franklin College (Indiana)','Indiana University of Pennsylvania','York University','Ohio Wesleyan University','Northern Kentucky University','University of Akron','College of Wooster','Baldwin Wallace University','Cedarville University','Thiel College','Mount Vernon Nazarene University','University of Pittsburgh','University of Windsor','University of Michigan','Central Michigan University','Indiana University   Purdue University Indianapolis','Taylor University','Goshen College','Kenyon College','Pennsylvania State University','Carleton University','University of Michigan Dearborn','Washington & Jefferson College','Spring Arbor University','Ashland University','Case Western Reserve University','Western Michigan University','University of Western Ontario','Westminster College (Pennsylvania)','University of Cincinnati','Michigan State University','Saginaw Valley State University','Ohio University','Cleveland State University','Ryerson University','University of Toronto','Kalamazoo College','Denison University','Grand Valley State University','Kent State University','Youngstown State University','Fanshawe College','Oberlin College','Butler University','Duquesne University']


target_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']

max_offset = 0.15
offset = 0 if len(target_schools)==1 else max_offset/(len(target_schools)-1)


plt.figure()
for i,school in enumerate(target_schools):
    # Get years
    x = np.array(list(sorted(data[school])), dtype=float) 
    # Get bounds for each years
    rank_mn_mx = [min_max(data[school][year]) for year in x] 

    # Extract bounds
    y, y_span = zip(*rank_mn_mx) #unzip
    y, y_span = np.array(y), np.array(y_span)
    y_span -= y

    # Shift by offset
    x += i*offset-max_offset

    _,cap,_ = plt.errorbar(x, y, yerr=y_span, 
                         fmt='-o', elinewidth=2, markeredgewidth=2,
                         capsize=0, lolims=True, label=school)

    # Display ranks
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}  
    for i,j in zip(x,y):
        plt.annotate(str(j),xy=(i+0.02,j+0.6), **font)


    for c in cap: 
        c.set_marker("_")
        c.set_markersize(10)


ax = plt.gca()
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax.legend(handles, labels)

title_font = {'weight' : 'bold',
              'size'   : 20} 

plt.xticks(years)
plt.yticks(range(0,int(plt.ylim()[1]),5))
plt.title("ICPC ECNA Regional Comparison", **title_font)
plt.xlabel("Year")
plt.ylabel("Rank")
plt.show()
        


