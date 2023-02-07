import sys
sys.path.append('../')
import system.global_value as g

import slack.send as send
import slack.receive as receive
import agent.agent_action_func as act
import agent.agent_deduce_func as deduce

def night(gameid):
    print("night:"+str(gameid))

    with g.connection.cursor() as cur:
        cur.execute("select * from characters where player=0 and life=0 and game_id="+str(gameid))
        characters=cur.fetchall()

    # 夜を通知するメッセージの送信
    text=[0,0,0,0,100,0,0]
    send.send(gameid, text)
    receive.receive(gameid)

    # エージェントの行動
    for i in characters:
        act.act(gameid, i[1])

    # エージェントの推理
    for j in characters:
        deduce.deduce(gameid, j[1])
