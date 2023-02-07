import sys
sys.path.append('../')
import system.global_value as g


print("")
### テスト用 ###

##########

with g.connection.cursor() as cur:
    cur.execute("select * from slack order by id desc limit 1")
    slack=cur.fetchone()

import system.start_func as start
start.start(slack[0])
