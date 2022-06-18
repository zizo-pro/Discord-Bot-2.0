import sqlite3
db = sqlite3.connect("bot_database.db")
cr = db.cursor()
###################################################

###################################################
def get_bad_words():
    cr.execute("SELECT bad_word FROM bad_words")
    data = cr.fetchall()
    Blocked_Words = []
    for i in range(len(data)):
        Blocked_Words.append(data[i][0])
    return Blocked_Words
###################################################

###################################################
def get_id(user_name):
    cr.execute(f"SELECT id FROM users WHERE user_name = '{user_name}'")
    it = cr.fetchone()
    id = it[0]
    return id
###################################################

###################################################
def get_user_name(id):
    sqlite3.connect("bot_database.db").cursor().execute(f"SELECT user_name FROM users WHERE id = '{id}'")
    user_ame = sqlite3.connect("bot_database.db").cursor().fetchone()
    user_name = user_ame[0]
    return user_name
###################################################

###################################################
def get_users_from_db():
    cr.execute("SELECT id FROM users")
    lol = cr.fetchall()
    users = []
    for i in range(len(lol)):
        users.append(lol[i][0])
    return users
###################################################

###################################################
def get_user_XP_LVL(ig):
    cr.execute(f"SELECT XP,lvl FROM ranks WHERE id = '{ig}'")
    xpdata = cr.fetchone()
    return xpdata
###################################################