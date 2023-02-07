import sys
sys.path.append('../')
import system.global_value as g

import slack.send as send

import requests
import json
import MySQLdb
import time

def wait_player_message():
    while True:
        r = requests.get(url, headers=headers, params=params)
        json_data = r.json()
        msgs = json_data['messages'][0]

        if ('user' in msgs):    # in演算子でjson内にusernameというkeyがあるならTrue、ないならFalse
            user_name = msgs['user']
            if (user_name == user_id):
                text_content = msgs['text']
                print("入力完了")
                return text_content
        
        print("入力待ち")
        time.sleep(5)

import re

def change(comment):
    game_id = games[0]
    day = games[1]
    src = 0
    #プレイヤー抽出
    player = re.findall("[A-Z]", comment)
    #私だけを抽出
    I = re.findall("私は",comment)
    #占った結果だけを抽出
    divination = re.findall("占った結果", comment)

    #プレイヤー名が存在している場合
    if player:
        if re.findall("怪しい", comment):
            return [game_id, day, src, player[0], 2, 0, 99]
        elif re.findall("怪しくない", comment):
            return [game_id, day, src, player[0], 2, 1, 99]
        elif re.findall("信じられる", comment):
            return [game_id, day, src, player[0], 3, 0, 99]
        elif re.findall("信じられない", comment):
            return [game_id, day, src, player[0], 3, 1, 99]
        elif re.findall("投票します", comment):
            return [game_id, day, src, player[0], 4, 99, 99]
    #プレイヤー名が存在していない場合
    elif I:
        #役職を抽出
        director = re.findall("[一-龥]", comment)
        #人狼の場合
        if "人" == director[1]:
            return [game_id, day, src, player[0], 1, 99, 0]
            #村人の場合
        elif "村" == director[1]:
            return [game_id, day, src, player[0], 1, 99, 1]
        #占い師の場合
        elif "占" == director[1]:
            return [game_id, day, src, player[0], 1, 99, 2]
    #占った結果
    elif divination:
        director = re.findall("[一-龥]", comment)
        #人狼の場合
        if "人" == director[3]:
            return [game_id, day, src, player[0], 5, 99, 0]
        #村人の場合
        elif "村" == director[3]:
            return [game_id, day, src, player[0], 5, 99, 1]
        #占い師の場合
        elif "占" == director[3]:
            return [game_id, day, src, player[0], 5, 99, 2]

def receive(gameid):
    print("called receive")

    global slack
    with g.connection.cursor() as cur:
        cur.execute("select * from slack where id="+str(gameid))
        slack=cur.fetchone()

    global url, headers, params, user_id
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": "Bearer "+slack[4]}
    params = {
       "channel": slack[3],
       "limit": 1
    }
    user_id = slack[5]

    global games
    with g.connection.cursor() as cur:
        cur.execute("select * from games where game_id="+str(gameid))
        games=cur.fetchone()

    global characters
    with g.connection.cursor() as cur:
        cur.execute("select * from characters where game_id="+str(gameid))
        characters=cur.fetchall()

    player_action="no data"
    print(games)

    if (int(games[2])==0):
        if (int(characters[0][3])==1):
            return
        player_action = wait_player_message()
        convert = lambda c: ord(c) - ord('A')

        text=[0,0,0,0,100,1,convert(player_action)]
        send.send(gameid, text)

    elif (int(games[2])==1):
        player_action = wait_player_message()
    elif (int(games[2])==2):
        player_action = wait_player_message()
        convert = lambda c: ord(c) - ord('A')
        return convert(player_action)
