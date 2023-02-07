import sys
sys.path.append('../')
import system.global_value as g

import slack.send as send

def end(gameid):
    # ゲーム終了時の処理　
    text=[0,0,0,0,110,1,0]
    send.send(gameid, text)

    return
    