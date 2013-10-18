"""
Read in all pickled things in saves/*, process from there

"""

import os
import pickle
import re
import string
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
                songs[key]['weeks'] = 1
                songs[key]['last'] = date
    return songs
    
        
def update_song(songs, key, song, date):
    try:
        songs[key]['relative'] += 41 - int(song["position"])
    except:
        print songs[key]
        traceback.print_exc()
    songs[key]['peak'] = min(int(songs[key]['peak']), int(song['peak']))
    songs[key]['twc'] = max(int(songs[key]['twc']), int(song['twc']))
    songs[key]['first'] = min(songs[key]['first'], date)
    songs[key]['last'] = max(songs[key]['last'], date)
    songs[key]['weeks'] += 1
    return songs
    
def sanitize_song(name):
    trans = string.maketrans("\t\n\r", "   ")
    return str(name).translate(trans)
    
    
def output(songs):
    print "first\tlast\tpeak\trelative\tweeks\tkey"
    for k,v in songs.items():
        k = sanitize_song(k)
        v["key"] = k
        print "%(first)s\t%(last)s\t%(peak)s\t%(relative)s\t%(weeks)s\t%(key)s" % v
        

if __name__ == "__main__":
    results = read_all_the_things()
    songs = compile(results)
    output(songs)

