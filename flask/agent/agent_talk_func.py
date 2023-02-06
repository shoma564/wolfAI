import sys
sys.path.append('../')
import system.global_value as g

def talk(gameid, charid):
    print("talk"+str(gameid)+":"+str(charid))
    text=[gameid, 0, charid, charid, 1, 0, 0]
    return text