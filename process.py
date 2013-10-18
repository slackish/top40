"""
Read in all pickled things in saves/*, process from there

week is a list of singles:
                { "artist": artists[i],
                   "song": songs[i],
                   "position": attrs[i*4],
                   "peak": attrs[i*4 + 1],
                   "weeks": attrs[i*4 + 2],
                   "twc": attrs[i*4 + 3],
                 }
"""

import os
import pickle
import re
import traceback


def read_all_the_things():
    firere = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    results = {}

    for f in os.listdir("saves"):
        try:
            if not firere.match(f):
                continue
            results[f] = pickle.load(open("saves/%s" % f, "rb"))
        except:
            traceback.print_exc()
    return results



def compile(results):
    songs = {}
    for date,week in results.items():
        for song in week:
            key = "%s-%s" % (song["artist"], song["song"])
            if key in songs:
                songs = update_song(songs, key, song, date)
            else:
                songs[key] = song
                try:
                    songs[key]['relative'] = 41 - int(song["position"])
                except:
                    print key, songs['key']
                    traceback.print_exc()
                songs[key]['first'] = date
                songs[key]['last'] = date
    return songs
    
        
def update_song(songs, key, song, date):
    try:
        songs[key]['relative'] += 41 - int(song["position"])
    except:
        print songs[key]
        traceback.print_exc()
    songs[key]['peak'] = max(int(songs[key]['peak']), int(song['peak']))
    songs[key]['twc'] = max(int(songs[key]['twc']), int(song['twc']))
    songs[key]['first'] = min(songs[key]['first'], date)
    songs[key]['last'] = max(songs[key]['last'], date)
    return songs
    
    
def output(songs):
    print "key, peak, first, last, peak, relative"
    for k,v in songs.items():
        v["key"] = k
        print "%(key)s, %(peak)s, %(first)s, %(last)s, %(peak)s, %(relative)s" % v
        



if __name__ == "__main__":
    results = read_all_the_things()
    songs = compile(results)
    output(songs)

