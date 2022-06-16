import sqlite3
###################################################

###################################################
def get_bad_words():
    global Blocked_Words
    sqlite3.connect("bot_database.db").cursor().execute("SELECT bad_word FROM bad_words")
    data = sqlite3.connect("bot_database.db").cursor().fetchall()
    Blocked_Words = []
    for i in range(len(data)):
        Blocked_Words.append(data[i][0])
get_bad_words()
###################################################

###################################################
def get_id(user_name):
    sqlite3.connect("bot_database.db").cursor().execute(f"SELECT id FROM users WHERE user_name = '{user_name}'")
    it = sqlite3.connect("bot_database.db").cursor().fetchone()
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
    global users
    sqlite3.connect("bot_database.db").cursor().execute("SELECT id FROM users")
    lol = sqlite3.connect("bot_database.db").cursor().fetchall()
    users = []
    for i in range(len(lol)):
        users.append(lol[i][0])
get_users_from_db()
###################################################

###################################################
def get_user_XP_LVL(ig):
    sqlite3.connect("bot_database.db").cursor().execute(f"SELECT XP,lvl FROM ranks WHERE id = '{ig}'")
    xpdata = sqlite3.connect("bot_database.db").cursor().fetchone()
    return xpdata
###################################################