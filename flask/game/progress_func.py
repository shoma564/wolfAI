import sys
sys.path.append('../')
import system.global_value as g

import game.night_func as night
import game.noon_func as noon
import game.vote_func as vote
import system.pause_func as pause
import system.end_func as end

# 全部ここから呼び出す
def progress(gameid):
    while(True):

        with g.connection.cursor() as cur:
            cur.execute("select * from games where game_id="+str(gameid))
            games=cur.fetchone()

        data = {
            'day'       : int(games[1])+1 if int(games[2])==0 else int(games[1]),
            'phase'     : (int(games[2])+1)%3,
            'gameid'    : gameid
        }

        if (games[2]>30):
            pause.pause(gameid)
            break

        elif (games[2]==0):
            night.night(gameid)
            with g.connection.cursor() as cur:
                cur.execute(g.update_games, data)
                g.connection.commit()

        elif (games[2]==1):
            noon.noon(gameid)
            with g.connection.cursor() as cur:
                cur.execute(g.update_games, data)
                g.connection.commit()

        elif (games[2]==2):
            vote.vote(gameid)
            with g.connection.cursor() as cur:
                cur.execute(g.update_games, data)
                g.connection.commit()

        # ゲーム終了条件の確認
        with g.connection.cursor() as cur:
            cur.execute("select * from characters where game_id="+str(gameid))
            characters=cur.fetchall()

        if (int(characters[0][5])==1):
            # プレイヤーの敗北
            with g.connection.cursor() as cur:
                cur.execute("UPDATE games set phase=60 WHERE game_id="+str(gameid))
                g.connection.commit()
            end.end(gameid)
            break

        living_wolves = 0
        living_villagers = 0
        for i in range(len(characters)-1):
            if (int(characters[i][3])==0 and int(characters[i][5])==0):
                living_wolves += 1
            elif (int(characters[i][3])!=0 and int(characters[i][5])==0):
                living_villagers += 1
        if (living_wolves == 0):
            # 村人陣営の勝利
            with g.connection.cursor() as cur:
                cur.execute("UPDATE games set phase=40 WHERE game_id="+str(gameid))
                g.connection.commit()
            end.end(gameid)
            break

        elif (living_wolves >= living_villagers):
            with g.connection.cursor() as cur:
                cur.execute("UPDATE games set phase=50 WHERE game_id="+str(gameid))
                g.connection.commit()
            end.end(gameid)       
            break     

