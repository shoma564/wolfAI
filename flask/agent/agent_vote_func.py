import sys
sys.path.append('../')
import system.global_value as g

def agent_vote(gameid, charid, recollect):
    with g.connection.cursor() as cur:
        cur.execute("select * from deduces where life=0 and game_id="+str(gameid)+" and char_id="+str(charid))
        characters=cur.fetchall()

    characters=list(characters)
    characters.sort(key=lambda x:x[3], reverse=True)
    agent_vote=characters[0][2]
    if recollect:
        for j in characters:
            for i in recollect:
                if(j[2]==i):
                    break
            if(j[2]==i):
                break
        agent_vote=j[2]

    return agent_vote