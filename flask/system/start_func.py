import sys
sys.path.append('../')
import system.global_value as g
import random

# 各役職の人数の初期化
werewolf_player = 0
villager_player = 0
diviner_player = 0 

def start(gameid):
    print(gameid)
    ### 役職定義 ###
    # 役の割り振り
    player = 10                                             # プレイヤー人数の定義
    job_balance = [player*0.2, player*0.8, player*0.2]      # 役職の割合の定義

    # 役職の割り振りの関数
    # 役職が決めた割合（job_balance）になるように調整
    # 人狼:0, 村人:1, 占い師:2
    def job_distribution(a):
        global werewolf_player, villager_player, diviner_player
        r = random.randint(0,2)
        if r == 0:
            werewolf_player += 1
            if werewolf_player > job_balance[0]:
                werewolf_player -= 1
                r = job_distribution(a)
        elif r == 1:
            villager_player += 1
            if villager_player > job_balance[1]:
                villager_player -= 1
                r = job_distribution(a)
        elif r == 2:
            diviner_player += 1
            if diviner_player > job_balance[2]:
                diviner_player -= 1
                r = job_distribution(a)
        return r

    # プレイヤー情報を定義した配列
    characters = [{
        "game_id":int(gameid), 
        "char_id":i, 
        "name":chr(ord('A')+i), 
        "position":job_distribution(i), 
        "player":1 if i==0 else 0, 
        "life":0
        } for i in range(player)]

    ####################

    ### 推理定義 ###
    inference = [{
        "game_id":int(gameid), 
        "char_id":i, 
        "target":j if j<i else j+1, 
        "deduce_wolf":random.randint(21,80), 
        "deduce_villager":random.randint(21,80), 
        "deduce_seer":random.randint(21,80), 
        "trust":random.randint(21,80), 
        "life":0
        } for i in range(1, player) for j in range(0, player-1)]

    ####################

    ### 時間定義 ###
    games = {"game_id":int(gameid), "day":0, "phase":0}

    ####################

    ### db格納 ###
    with g.connection.cursor() as cur:
        cur.executemany(g.insert_characters, characters)
        g.connection.commit()

    with g.connection.cursor() as cur:
        cur.executemany(g.insert_deduces, inference)
        g.connection.commit()
    
    with g.connection.cursor() as cur:
        cur.execute(g.insert_games, games)
        g.connection.commit()
    ####################

    ### progress関数呼び出し ###
    import game.progress_func as progress
    progress.progress(gameid)

    ####################