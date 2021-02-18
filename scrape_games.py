#!/usr/bin/python -u

import os
import json
import urllib.request
import os.path as osp

OUT_DIR = osp.join(os.sep, "d:", "Other", "hanabi_replays")

def save_json(json_obj, outfile):
    with open(outfile, 'w') as of:
        json.dump(json_obj, of, indent=2)


if __name__=='__main__':
    print("saving games to: ", OUT_DIR)
    for game_id in range(10001, 440435):
        print("downloading game: {}".format(game_id), end='\r')
        try:
            with urllib.request.urlopen("https://hanab.live/export/{0:06d}".format(game_id)) as url:
                data = json.loads(url.read().decode())
                save_json(data, osp.join(OUT_DIR, "game_{0:06d}.json".format(game_id)))
        except urllib.error.HTTPError:
            print("could not find game {}".format(game_id))
