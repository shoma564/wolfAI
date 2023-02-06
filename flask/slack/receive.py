import sys
sys.path.append('../')
import system.global_value as g

import requests
import json
import MySQLdb

def receive(gameid):
    print("called receive")

    with g.connection.cursor() as cur:
        cur.execute("select * from games where game_id="+str(gameid))
        games=cur.fetchone()

    if (int(games[2])==2):
        player_vote=1
        return player_vote