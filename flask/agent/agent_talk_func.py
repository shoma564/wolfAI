import sys
sys.path.append('../')
import system.global_value as g

# MySQLdbのインポート
import MySQLdb
import random

def connect():
    # データベースへの接続とカーソルの作成
    connection = MySQLdb.connect(
    host='mysql',
    user='root',
    passwd='root',
    db='slack')
    return connection

def deconnect(connection):
    # 保存をする
    connection.commit()
    # 接続を閉じる
    connection.close()
    return
    
# 村人の発言内容
def villager_deduce(game_id,char_id,day):
    connection = connect()
    cursor = connection.cursor()
    if day == 1:
        comment = [ game_id, day, char_id, 99 , 1 , 99 , 1]
    elif day >= 2:
        # 人狼と村人と占い師の値がそれぞれ最大のものをとってくる。重複クエリは削除されない
        select = "SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_wolf = (SELECT MAX(deduce_wolf) FROM deduces) UNION  ALL SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_villager = (SELECT MAX(deduce_villager) FROM deduces) UNION ALL SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_seer = (SELECT MAX(deduce_seer) FROM deduces)"
        select_wolf = "SELECT game_id, char_id, target, max(deduce_wolf) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"
        select_villager = "SELECT game_id, char_id, target, max(deduce_villager) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"
        select_seer = "SELECT game_id, char_id, target, max(deduce_seer) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"

        cursor.execute(select_wolf)
        result = cursor.fetchall()
        wolf_value = result[3]
        cursor.execute(select_villager)
        result = cursor.fetchall()
        village_value = result[3]
        cursor.execute(select_seer)
        result = cursor.fetchall()
        seer_value = result[3]

        deconnect(connection)

        if wolf_value >= village_value and wolf_value >= seer_value:
            comment = [ game_id, day, char_id, result[0][2], 2, 0, 99]
        elif village_value >= wolf_value and village_value >= seer_value:
            comment = [ game_id, day, char_id, result[1][2], 3, 0, 99]
        elif seer_value >= wolf_value and seer_value >= village_value:
            comment = [ game_id, day, char_id, result[2][2], 3, 0, 99]
    
    return comment
    

# 人狼の発言内容
def wolf_deduce(game_id,char_id,day):
    connection = connect()
    cursor = connection.cursor()
    if day == 1:
        comment = [ game_id, day, char_id, 99 , 1 , 99 , 1]
    elif day >= 2:
        # 人狼と村人と占い師の値がそれぞれ最大のものをとってくる。重複クエリは削除されない
        select = "SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_wolf = (SELECT MAX(deduce_wolf) FROM deduces) UNION  ALL SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_villager = (SELECT MAX(deduce_villager) FROM deduces) UNION ALL SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_seer = (SELECT MAX(deduce_seer) FROM deduces)"
        select_wolf = "SELECT game_id, char_id, target, max(deduce_wolf) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"
        select_villager = "SELECT game_id, char_id, target, max(deduce_villager) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"
        select_seer = "SELECT game_id, char_id, target, max(deduce_seer) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"

        cursor.execute(select_wolf)
        result = cursor.fetchall()
        wolf_value = result[3]
        cursor.execute(select_villager)
        result = cursor.fetchall()
        village_value = result[3]
        cursor.execute(select_seer)
        result = cursor.fetchall()
        seer_value = result[3]

        deconnect(connection)
        
        if wolf_value >= village_value and wolf_value >= seer_value:
            if seer_value >= village_value:
                comment = [ game_id, day, char_id, result[2][2], 2, 0, 99]    
            elif village_value >= seer_value:
                comment = [ game_id, day, char_id, result[1][2], 3, random.randint(0,1) , 99]
        elif village_value >= wolf_value and village_value >= seer_value:
            comment = [ game_id, day, char_id, result[1][2], random.randint(2,3), random.randint(0,1), 99]
        elif seer_value >= wolf_value and seer_value >= village_value:
            comment = [ game_id, day, char_id, result[2][2], random.randint(2,3), random.randint(0,1), 99]
    

    return comment
# 占い師の発言内容
def seer_deduce(game_id,char_id,day):
    connection = connect()
    cursor = connection.cursor()

    #占った結果を発言させたい
    if day == 1:
        comment = [ game_id, day, char_id, 99 , 1 , 99 , 1]
    elif day >= 2:
        # 人狼と村人と占い師の値がそれぞれ最大のものをとってくる。重複クエリは削除されない
        select = "SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_wolf = (SELECT MAX(deduce_wolf) FROM deduces) UNION  ALL SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_villager = (SELECT MAX(deduce_villager) FROM deduces) UNION ALL SELECT * FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0 AND deduce_seer = (SELECT MAX(deduce_seer) FROM deduces)"
        select_wolf = "SELECT game_id, char_id, target, max(deduce_wolf) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"
        select_villager = "SELECT game_id, char_id, target, max(deduce_villager) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"
        select_seer = "SELECT game_id, char_id, target, max(deduce_seer) FROM deduces WHARE game_id=" + str(game_id) + " AND char_id=" + str(char_id) + " AND life = 0"

        cursor.execute(select_wolf)
        result = cursor.fetchall()
        wolf_value = result[3]
        cursor.execute(select_villager)
        result = cursor.fetchall()
        village_value = result[3]
        cursor.execute(select_seer)
        result = cursor.fetchall()
        seer_value = result[3]

        deconnect(connection)

        if wolf_value >= village_value and wolf_value >= seer_value:
            comment = [ game_id, day, char_id, result[0][2], 2, 0, 99]
        elif village_value >= wolf_value and village_value >= seer_value:
            comment = [ game_id, day, char_id, result[1][2], 3, 0, 99]
        elif seer_value >= wolf_value and seer_value >= village_value:
            if wolf_value >= village_value:
                comment = [ game_id, day, char_id, result[0][2], 2, 0, 99]
            elif village_value >= seer_value:
                comment = [ game_id, day, char_id, result[0][2], 3, 0, 99]
    

    return comment

def talk(game_id,char_id):
    connection = connect()
    cursor = connection.cursor()
    # 日付を取得するSQL
    select_day = "SELECT * FROM games WHERE game_id =" + str(game_id)
    cursor.execute(select_day)
    day=cursor.fetchone()
    # char_idから役職を判断するSQL分の作成
    select = "SELECT * FROM characters WHERE game_id =" + str(game_id) +" AND char_id =" + str(char_id)
    cursor.execute(select)
    agent_job=cursor.fetchone()
    deconnect(connection)
    if agent_job[3] == 0:
        return wolf_deduce(game_id, char_id, day[1])
    elif agent_job[3] == 1:
        return villager_deduce(game_id, char_id, day[1])
    elif agent_job[3] == 2:
        return seer_deduce(game_id, char_id, day[1])