import sys
sys.path.append('../')
import system.global_value as g

import random

import slack.send as send
import slack.receive as receive
import agent.agent_talk_func as talk
import agent.agent_deduce_func as deduce

def noon(gameid):
    print("noon:"+str(gameid))
    # 昼を通知する
    # 犠牲者を通知する
    text=[0,0,0,0,11,0,0]
    send.send(gameid, text)

    # 会話
    with g.connection.cursor() as cur:
        cur.execute("select * from characters where life=0 and game_id="+str(gameid))
        characters=cur.fetchall()

    random_chara=random.sample(characters, len(characters))
    for i in random_chara:
        if (i[1]==0):
            text=[0,0,0,0,11,1,0]
            send.send(gameid, text)
            receive.receive(gameid)
        else :
            text=talk.talk(gameid, i[1])
            send.send(gameid, text)
        for j in characters:
            if (j[1]==0):
                pass
            else:
                deduce.deduce(gameid, j[1])
            