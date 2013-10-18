"""
Read in all pickled things in saves/*, process from there
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
            results[f] = pickle.load(f, "rb")
        except:
            traceback.print_exc()
    return results

    



if __name__ == "__main__":
    main()
