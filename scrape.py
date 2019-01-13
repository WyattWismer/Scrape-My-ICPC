from collections import defaultdict as dd
from bs4 import BeautifulSoup
from urllib2 import Request,urlopen
import numpy as np
import pickle
import re
import os


#CONSTANTS
page_dir = "pages"

def clean_school_name(school):
    """
    Clean school name to meet size requirements
    """
    school = school.strip()
    # Remove multiple spaces
    school = ' '.join(school.split())
    # cap exceptionally long strings
    cap = 30 
    if len(school)>cap:
        end='...'
        school = school[:cap-len(end)]+end
    return school

def in_dir(fname, path_to_dir='.'):
    """
    Checks if file is in given directory
    """
    return fname in os.listdir(path_to_dir) 

def GET_page(year):
    """
    Makes HTTP request to obtain kattis standings page 
    """
    # Build request
    year_str = str(year%100)
    pattern_str = "https://ecna%s.kattis.com/standings" 
    url = pattern_str % year_str

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    # GET page
    req = Request(url, headers=hdr)
    page = urlopen(req).read()
    page = re.sub(r'[^\x00-\x7F]+',' ', page) # Remove non-ascii
    return page

def load_page(year):
    """
    If already present loads kattis standing page from memory.
    Otherwise makes a request to retrieve page and store for later. 
    """
    # Make page_dir if it doesn't already exist
    if not in_dir(page_dir):
        os.mkdir(page_dir)

     # Check for saved pages
    page_name = "%d.html" % year
    page_pth = os.path.join(page_dir, page_name)
    
    # Check for existing page
    if in_dir(page_name, page_dir):
        fl = open(page_pth, 'r')
        return pickle.load(fl)
    
    # Page not on disk, make request
    page = GET_page(year)

    # Pickle it!
    fl = open(page_pth, 'w')
    pickle.dump(page, fl)
    return page


def get_soup(year):
    """
    Builds a *beautiful* soup
    """
    # Construct soup 
    page = load_page(year)
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_standings(year):
    """
    Scrapes all the standings for a particular year
    """
    soup = get_soup(year)
    teams = dd(list)
    
    # get rid of thead
    soup.find(id="standings").thead.decompose()

    # iterate through teams
    for team in soup.find(id="standings").find_all("tr"):
        if not team.find("td", {"class": "rank table-min-wrap"}):
            # Can't find rank, indicates that we've hit the bottom of the table
            break

        rank = int(team.find("td", {"class": "rank table-min-wrap"}).string)
        school = team.find("td", {"class": "university-logo table-min-wrap"}).img['alt']
        school = clean_school_name(school)
        
        teams[school].append(rank)
    return teams






