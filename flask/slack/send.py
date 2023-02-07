import sys
sys.path.append('../')
import system.global_value as g

import requests     # pip install requests
import json

import time

def system_message(message):
    requests.post(WEB_HOOK_URL, data=json.dumps({
        "channel" : channel_name,
        "text" : message,
        "icon_emoji" : ":gear:",
        "username" : "SYSTEM"
    }))

def agent_message(message, text):
    requests.post(WEB_HOOK_URL, data=json.dumps({
        "channel" : channel_name,
        "text" : message,
        "icon_emoji" : ":hugging_face:",
        "username" : characters[text[2]][2]
    }))

def send(gameid, text):
    print("called send")
    print(text)
    with g.connection.cursor() as cur:
        cur.execute("select * from slack where id="+str(gameid))
        slack=cur.fetchone()

    with g.connection.cursor() as cur:
        cur.execute("select * from games where game_id="+str(gameid))
        games=cur.fetchone()

    global characters
    with g.connection.cursor() as cur:
        cur.execute("select * from characters where game_id="+str(gameid))
        characters=cur.fetchall()

    global WEB_HOOK_URL, channel_name
    WEB_HOOK_URL = slack[1]
    channel_name = slack[2]

    if (int(text[4])==100):
        if (int(text[5])==0):
            # 夜の通知とアクションの問いかけ
            if (int(characters[0][3])==0):
                with g.connection.cursor() as cur:
                    cur.execute("select * from characters where char_id!=0 and position=0 and game_id="+str(gameid))
                    comrade = cur.fetchone()
                with g.connection.cursor() as cur:
                    cur.execute("select * from characters where life=0 and position!=0 and game_id="+str(gameid))
                    candidate_list = cur.fetchall()
                candidate = [candidate_list[i][2] for i in range(len(candidate_list))]
                name=' '.join(candidate)
                message=str(games[1])+"日目の夜になりました。\nあなたは人狼です。殺したい人を一人選択してください。\nあなたの仲間："+str(comrade[2])+"\n候補："+name
            elif (int(characters[0][3])==1):
                message=str(games[1])+"日目の夜になりました。\nあなたは村人です。できる行動はありません。"
            elif (int(characters[0][3])==2):
                with g.connection.cursor() as cur:
                    cur.execute("select * from characters where char_id!=0 and life=0 and game_id="+str(gameid))
                    candidate_list = cur.fetchall()
                candidate = [candidate_list[i][2] for i in range(len(candidate_list))]
                name=' '.join(candidate)
                message=str(games[1])+"日目の夜になりました。\nあなたは占い師です。占いたい人を一人選択してください。\n候補："+name
        
        elif (int(text[5])==1):
            # 結果の通知
            if (int(characters[0][3])==0):
                wolf_action=text[6]
                with g.connection.cursor() as cur:
                    cur.execute("UPDATE characters SET life="+str(int(games[1])+1)+" WHERE game_id="+str(gameid)+" and char_id="+str(wolf_action))
                    cur.execute("UPDATE deduces SET life="+str(int(games[1])+1)+" WHERE game_id="+str(gameid)+" and target="+str(wolf_action))
                    g.connection.commit()
                message=str(characters[int(text[6])][2])+"を殺しました" 

            elif (int(characters[0][3])==2):
                if (int(characters[text[6]][3])==0):
                    message=str(characters[text[6]][2])+"は人狼です。"
                if (int(characters[text[6]][3])==1):
                    message=str(characters[text[6]][2])+"は村人です。"
                if (int(characters[text[6]][3])==2):
                    message=str(characters[text[6]][2])+"は占い師です。"

        system_message(message)

    elif (int(text[4])==110):
        if (int(text[5])==0):
            # 昼の通知と死人の通知
            with g.connection.cursor() as cur:
                cur.execute("select * from characters where game_id="+str(gameid)+" and life="+str(games[1]))
                death=cur.fetchone()
            message=str(games[1])+"日目の昼になりました。\n本日の犠牲者は、"+str(death[2])+"です。"

        elif (int(text[5])==1):
            # 発言の問いかけ
            message="発言を選んでください。"
    
        system_message(message)
    
    elif (int(text[4])==120):
        if (int(text[5])==0):
            # 投票の通知
            message=str(games[1])+"日目の投票になりました。"

        elif (int(text[5])==1):
            # 誰に投票するか
            with g.connection.cursor() as cur:
                cur.execute("select * from characters where char_id!=0 and life=0 and game_id="+str(gameid))
                candidate_list = cur.fetchall()
            candidate = [candidate_list[i][2] for i in range(len(candidate_list))]
            name=' '.join(candidate)
            message="投票先を選んでください。\n候補:"+name
        
        elif (int(text[5])==2):
            # 投票結果
            message=str(characters[text[6]][2])+"が処刑されます。"
        
        elif (int(text[5])==3):
            # 決選投票の通知
            namelist=[characters[i][2] for i in text[6]]
            name=' '.join(namelist)
            message="候補者が二人以上いるため、決戦投票を行います。\n候補："+name

        system_message(message)

    elif (int(text[4])==130):
        # 終了の通知
        if (int(games[2])==40):
            message="村人陣営の勝利です。"
        elif (int(games[2])==50):
            message="人狼陣営の勝利です。"
        elif (int(games[2])==60):
            message="プレイヤーが死亡しました。"

        system_message(message)

    else :
        message="default"
        # エージェントメッセージ
        # 1. 私は{役職}です。
        if (int(text[4])==1):
            if (int(text[6])==0):
                message="私の役職は人狼です。"
            elif (int(text[6])==1):
                message="私の役職は村人です。"
            elif (int(text[6])==2):
                message="私の役職は占い師です。"
        # 2. {プレイヤー}は（怪しい/怪しくない）
        elif (int(text[4])==2):
            if (int(text[5])==0):
                message=str(characters[text[3]][2])+"は怪しい。"
            elif (int(text[5])==1):
                message=str(characters[text[3]][2])+"は怪しくない。"
        # 3. {プレイヤー}は（信じられる/信じられない）
        elif (int(text[4])==3):
            if (int(text[5])==0):
                message=str(characters[text[3]][2])+"は信じられる。"
            elif (int(text[5])==1):
                message=str(characters[text[3]][2])+"は信じられない。"
        # 4. {プレイヤー}に投票します。
        elif (int(text[4])==4):
            message=str(characters[text[3]][2])+"に投票します。"
        # 5. 占った結果、{プレイヤー}は{役職}でした。
        elif (int(text[4])==4):
            if (int(text[6])==0):
                message="占った結果、"+str(characters[text[3]][2])+"は人狼でした。"
            elif (int(text[6])==1):
                message="占った結果、"+str(characters[text[3]][2])+"は村人でした。"
            elif (int(text[6])==2):
                message="占った結果、"+str(characters[text[3]][2])+"占い師でした。"
        else :
            pass
        print(message)
        agent_message(message, text) 

    time.sleep(2)
