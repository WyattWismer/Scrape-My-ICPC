from collections import defaultdict as dd
from bs4 import BeautifulSoup
from urllib2 import Request,urlopen
import numpy as np
import re


def get_page(year):
    year_str = str(year%100)
    pattern_str = "https://ecna%s.kattis.com/standings" 
    url = pattern_str % year_str

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    req = Request(url, headers=hdr)
    page = urlopen(req).read()
    page = re.sub(r'[^\x00-\x7F]+',' ', page) # Remove non-ascii
    return page


def get_soup(year):
    page = get_page(year)
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_standings(year):
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

        teams[school].append(rank)
    return teams





