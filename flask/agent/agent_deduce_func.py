import sys
sys.path.append('../')
import system.global_value as g
import numpy as np

#deduce():
#夜;0, 昼:1, 投票:2

# def deduce_noon(id, char_id):
def deduce(id, char_id):
    #指定したidの推理データを取得
    with g.connection.cursor() as cur:
        cur.execute("select * from deduces where game_id="+str(id)+" and char_id="+str(char_id))
        data_deduce=cur.fetchall()

    with g.connection.cursor() as cur:
        cur.execute("select * from games where game_id="+str(id))
        games=cur.fetchone()

    with g.connection.cursor() as cur:
        cur.execute("select * from talks where game_id="+str(id)+" and day="+str(games[0]))
        data_talk_all=cur.fetchall()
    
    for data_talk in data_talk_all:
        if(data_talk[4]==1):
            target = data_talk[2]#src
            role = data[6]
            deduce_param = int(data_deduce[target-1][role+3]+(data_deduce[target-1][6]/2))
            data_deduce[target-1][role+3] = deduce_param if 255 > deduce_param else 255  
        

        elif(data_talk[4]==2):
            target = data_talk[3]
            option = data[5]
            deduce_param = int(data_deduce[target-1][3]+(data_deduce[target-1][6]/4))
            data_deduce[target-1][3] = deduce_param if 255 > deduce_param else 255

        elif(data_talk[4]==5):
            role = data[6]
            target = data_talk[3]
            if(random.random() < 0.5):
                deduce_param = int(data_deduce[target-1][role+3]+(data_deduce[target-1][6]/2))
                data_deduce[target-1][role+3] = deduce_param if 255 > deduce_param else 255
            else:
                deduce_param = int(data_deduce[target-1][role+3]-(data_deduce[target-1][6]/2))
                data_deduce[target-1][role+3] = deduce_param if 0 < deduce_param else 0

        for deduce_update in data_deduce:
            #ifにかからない時にDBの値を変に更新しちゃうかも
            with g.connection.cursor() as cur:
                cur.execute("update deduces set deduce_wolf="+str(deduce_update[3])+",deduce_villager="+str(deduce_update[4])+",deduce_seer="+str(deduce_update[4])+"  where game_id="+str(id)+" and char_id="+str(char_id)+" and target="+str(target))
                g.connection.commit()
    

# def deduce_night(id, char_id):
# 	cur_d.execute('select * from deduces where game_id=? and char_id=?', (id, char_id))
# 	data_night = cur_d.fetchone()


# #昼の処理
# for char_id in range(player):
#     例外の処理（割り込みなど）
#     deduce_noon(id, char_id, phase)
#     hatugen()

# #夜の処理
# for char_id in range(player):
#     deduce_night(id, char_id, phase)