import MySQLdb
import textwrap

# データベースへの接続
connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='root',
    db='slack')

# insert文の定義
insert_slack = textwrap.dedent("""\
    INSERT INTO slack (
        webhook_url, 
        Channel_name, 
        Channel_id, 
        token, 
        user, 
        sub_date
    ) VALUES (
        %(webhook_url)s,
        %(Channel_name)s,
        %(Channel_id)s,
        %(token)s,
        %(user)s,
        %(sub_date)s
    )
    """)

insert_characters = textwrap.dedent("""\
    INSERT INTO characters (
        game_id, 
        char_id,
        name, 
        position, 
        player, 
        life
    ) VALUES (
        %(game_id)s,
        %(char_id)s,        
        %(name)s,
        %(position)s,
        %(player)s,
        %(life)s
    )
    """)

insert_games = textwrap.dedent("""\
    INSERT INTO games (
        game_id, 
        day,
        phase
    ) VALUES (
        %(game_id)s,
        %(day)s,        
        %(phase)s
    )
    """)

insert_talks = textwrap.dedent("""\
    INSERT INTO talks (
        game_id,
        day,
        src,
        dst,
        text_id,
        opt,
        role
    ) VALUES (
        %(game_id)s,
        %(day)s,
        %(src)s,
        %(dst)s,
        %(text_id)s,
        %(opt)s,
        %(role)s
    )
    """)

insert_deduces = textwrap.dedent("""\
    INSERT INTO deduces (
        game_id,
        char_id,
        target,
        deduce_wolf,
        deduce_villager,
        deduce_seer,
        trust,
        life
    ) VALUES (
        %(game_id)s,
        %(char_id)s,
        %(target)s,
        %(deduce_wolf)s,
        %(deduce_villager)s,
        %(deduce_seer)s,
        %(trust)s,
        %(life)s
    )
    """)

### updateの定義
update_games = textwrap.dedent("""\
    UPDATE games set day=%(day)s, phase=%(phase)s WHERE game_id=%(gameid)s
    """)