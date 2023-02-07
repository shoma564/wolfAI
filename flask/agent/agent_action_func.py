import sys
sys.path.append('../')
import system.global_value as g

def act(gameid, charid):
    with g.connection.cursor() as cur:
        cur.execute("select * from games where game_id="+str(gameid))
        games=cur.fetchone()
    with g.connection.cursor() as cur:
        cur.execute("select * from characters where game_id="+str(gameid))
        characters=cur.fetchall()
    with g.connection.cursor() as cur:
        cur.execute("select * from deduces where life=0 and game_id="+str(gameid)+" and char_id="+str(charid))
        deduces=cur.fetchall()
    
    for i in characters:
        if (int(i[1])==charid):
            break

    # 人狼のアクション
    if(int(i[3])== 0):
        # 初日、味方の発見
        with g.connection.cursor() as cur:
            cur.execute("select * from characters where position=0 and game_id="+str(gameid))
            werewolf=cur.fetchall()
        if(int(games[1])==0):
            for k in werewolf:
                for j in werewolf:
                    if (k==j):
                        pass
                    else:
                        with g.connection.cursor() as cur:
                            cur.execute("UPDATE deduces SET deduce_wolf=255, deduce_villager=0, deduce_seer=0 WHERE game_id="+str(gameid)+" and char_id="+str(k[1])+" and target="+str(j[1]))
                            g.connection.commit()
        if (int(i[1])==int(werewolf[0][1]) or int(werewolf[0][5])!=0):
            with g.connection.cursor() as cur:
                cur.execute("select * from deduces where life=0 and game_id="+str(gameid)+" and char_id="+str(charid))
                deduces=cur.fetchall()
            deduces=list(deduces)
            deduces.sort(key=lambda x:x[5], reverse=True)

            # 殺しの処理
            wolf_action=deduces[0][2]
            with g.connection.cursor() as cur:
                cur.execute("UPDATE characters SET life="+str(int(games[1])+1)+" WHERE game_id="+str(gameid)+" and char_id="+str(wolf_action))
                cur.execute("UPDATE deduces SET life="+str(int(games[1])+1)+" WHERE game_id="+str(gameid)+" and target="+str(wolf_action))
                g.connection.commit()
        else :
            pass
    # 村人のアクション
    elif (int(i[3])== 1):
        pass
    # 占い師のアクション
    elif (int(i[3])== 2):
        with g.connection.cursor() as cur:
            cur.execute("select * from deduces where life=0 and game_id="+str(gameid)+" and char_id="+str(charid))
            deduces=cur.fetchall()
        deduces=list(deduces)
        deduces.sort(key=lambda x:x[3], reverse=True)

        for i in range(len(deduces)):
            if(deduces[i][3]!=255):
                break
        seer_action=deduces[i][2]

        if (int(characters[seer_action][3])==0): 
            with g.connection.cursor() as cur:
                cur.execute("UPDATE deduces SET deduce_wolf=255, deduce_villager=0, deduce_seer=0  WHERE game_id="+str(gameid)+" and char_id="+str(gameid)+" and target="+str(seer_action))
                g.connection.commit()
        elif (int(characters[seer_action][3])==1): 
            with g.connection.cursor() as cur:
                cur.execute("UPDATE deduces SET deduce_wolf=0, deduce_villager=255, deduce_seer=0  WHERE game_id="+str(gameid)+" and char_id="+str(gameid)+" and target="+str(seer_action))
                g.connection.commit()
        elif (int(characters[seer_action][3])==2): 
            with g.connection.cursor() as cur:
                cur.execute("UPDATE deduces SET deduce_wolf=0, deduce_villager=0, deduce_seer=255  WHERE game_id="+str(gameid)+" and char_id="+str(gameid)+" and target="+str(seer_action))
                g.connection.commit()            