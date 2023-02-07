import sys
sys.path.append('../')
import system.global_value as g

import collections

import slack.send as send
import slack.receive as receive
import agent.agent_vote_func as agent_vote

def vote(gameid):
    print("vote:"+str(gameid))

    with g.connection.cursor() as cur:
        cur.execute("select * from characters where life=0 and game_id="+str(gameid))
        characters=cur.fetchall()

    # 投票を通知
    text=[0,0,0,0,120,0,0]
    send.send(gameid, text)

    recollect=[]

    while (True):
        # 誰に投票するか
        text=[0,0,0,0,120,1,0]
        send.send(gameid, text)    
        if (int(characters[0][1])==0):
            player_vote = receive.receive(gameid)

        # 投票の処理
        vote_list=[0 for i in characters]
        num=0
        for i in characters:
            if i[1]==0:
                vote_list[num]=player_vote
            else:
                vote_list[num]=agent_vote.agent_vote(gameid, i[1], recollect)
            num+=1
        collection = collections.Counter(vote_list)
        print(collection.most_common())

        recollect=[]

        for i in collection.most_common():
            if (i[1] == collection.most_common()[0][1]):
                recollect.append(i[0])

        if (len(recollect)==1):
            # 投票者決定
            text=[0,0,0,0,120,2,recollect[0]]
            print(str(recollect[0]))
            # 殺しの処理
            with g.connection.cursor() as cur:
                cur.execute("UPDATE characters SET life=100 WHERE game_id="+str(gameid)+" and char_id="+str(recollect[0]))
                cur.execute("UPDATE deduces SET life=100 WHERE game_id="+str(gameid)+" and target="+str(recollect[0]))
                g.connection.commit()
            send.send(gameid, text)
            break

        # 決戦投票開始（誰と誰か）
        text=[0,0,0,0,120,3,recollect]
        send.send(gameid, text)
