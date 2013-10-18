"""
http://top40-charts.com/chart.php?cid=27&date=2013-10-19
"""

import os
import pickle
import random
import re
import requests
import time

from bs4 import BeautifulSoup

URL="http://top40-charts.com/chart.php?cid=27&date=%s"

def grab_url(url):
    r = requests.get(url)
    while r.status_code != 200:
        time.sleep(random.choice(range(10)))
        r = requests.get(url)
    return r.content


def beautify(content):
    return BeautifulSoup(content, "lxml")

def find_options(soup):
    """
    Those European fools (who admittedly have a "better" system)
    decided to reverse some crap around that made this function
    take 15 minutes longer than it should made this harder than 
    should of been.
    """
    options = soup.findAll("option")
    actualOptions = []
    for o in options:
        try:
            if "value" in o.attrs:
                friggenjerks = "-".join(o.string.split('-')[::-1])
                if o.attrs["value"] == str(friggenjerks):
                    actualOptions.append(str(o.attrs["value"]))
            else:
                continue
        except:
            # not really sure if this will do anything, but it the idea is to
            # put a wrapper on it
            continue
    return actualOptions


def get_artists(soup):
    return [x.text for x in soup.findAll("a", {"href": re.compile("^/artist.*")})]

def get_songs(soup):
    return [x.text for x in soup.findAll("a", {"href": re.compile("^/song.php*")}) if len(x.text) > 0]

def get_attrs(soup):
    return [x.text for x in soup.findAll("font", {"color": "384953"})]

def put_it_together(soup, date):
    artists = get_artists(soup)
    songs = get_songs(soup)
    attrs = get_attrs(soup)
    results = []
    for i in xrange(40):
        try:
            single = { "artist": artists[i],
                       "song": songs[i],
                       "position": i+1, 
                       "lw": attrs[i*4],
                       "peak": attrs[i*4 + 1],
                       "weeks": attrs[i*4 + 2],
                       "twc": attrs[i*4 + 3],
                     }
            results.append(single)
        except:
            print "something aint right with %s" % date
            traceback.format_exc()
            break
    return results
    

def process_options(options, soup, date):
    results = put_it_together(soup, date)
    save_file(results, date)
    random.shuffle(options)
    while len(options) > 0:
        date = options.pop()
        soup = beautify(grab_url(URL % date))
        results = put_it_together(soup, date)
        save_file(results, date)
        time.sleep(random.choice(range(10)) + 5)
        print "processed %s, %d to go" % (date, len(options))


def save_file(results, date):
    pickle.dump(results, open("saves/%s" % date, "wb"))
    
def filter_options(options):
    count = 0
    for i in os.listdir("saves/"):
        try:
            options.remove(i)
            count += 1
        except:
            continue
    print "Removed %d files to check" % count
    return options

def main():
    seed = "http://top40-charts.com/chart.php?cid=27&date=2013-10-19"
    date = "2013-10-19"
    soup = beautify(grab_url(seed))
    options = find_options(soup)
    options.remove(date)
    options = filter_options(options)
    process_options(options, soup, date)


if __name__ == "__main__":
    main()


