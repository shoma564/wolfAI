import sys
sys.path.append('../')
import system.global_value as g

### テスト用 ###
data = {
    'webhook_url'   : 'bbb',
    'Channel_name'  : 'bbb',
    'Channel_id'    : 'bbb',
    'token'         : 'bbb',
    'user'          : 'bbb',
    'sub_date'      : 'bbb'
}

with g.connection.cursor() as cur:
    cur.execute(g.insert_slack, data)
    g.connection.commit()

with g.connection.cursor() as cur:
    cur.execute("select * from slack order by id desc limit 1")
    slack=cur.fetchone()

##########

import system.start_func as start
start.start(slack[0])