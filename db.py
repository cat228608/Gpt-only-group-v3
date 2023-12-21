import sqlite3

def connect():
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    return conn, cursor
conn, cursor = connect()

def check_ban_user(chatid):
    cursor.execute(f"SELECT ban FROM users WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        cursor.execute(f"INSERT INTO users(user_id) VALUES ({chatid})")
        conn.commit()
        return '0'
    else:
        return row
 
def count():
    try:
        cursor.execute("SELECT COUNT(*) FROM token")
        row = cursor.fetchone()[0]
        if row == None:
            return 0
        conn.commit()
        return row
    except Exception as er:
        print(f'[ERROR] - {er}')
 
def set_status_work(arg):
    try:
        cursor.execute(f"SELECT {arg} FROM work")
        row = cursor.fetchone()
        conn.commit()
        if str(row[0]) == 'off':
            cursor.execute(f"UPDATE work SET {arg} = 'on'")
            conn.commit()
            return 'on'
        elif str(row[0]) == 'on':
            cursor.execute(f"UPDATE work SET {arg} = 'off'")
            conn.commit()
            return 'off'
    except Exception as er:
        print(f'[ERROR] - {er}')
        return 'error'
 
def get_status_work(arg):
    try:
        cursor.execute(f"SELECT work FROM work")
        row = cursor.fetchone()
        conn.commit()
        if str(row[0]) == 'off':
            return 'no work'
        else:
            cursor.execute(f"SELECT {arg} FROM work")
            row = cursor.fetchone()
            conn.commit()
            if row == None:
                return 'error'
            else:
                return row[0]
    except Exception as er:
        print(f'[ERROR] - {er}')
        return 'error'
    
def edit_limit(chatid, types, limit):
    if types == 'chat' or types == 'chats' or types == 'Chat' or types == 'Chats' or types == 'чат' or types == 'Чат':
        cursor.execute(f"SELECT limit_chat FROM config WHERE chat_id = {chatid}")
        row = cursor.fetchone()
        conn.commit()
        if row == None:
            cursor.execute(f"INSERT INTO config(chat_id, limit_chat) VALUES ({chatid}, {limit})")
            conn.commit()
            return 'good'
        else:
            cursor.execute(f"UPDATE config SET limit_chat = '{limit}' WHERE chat_id = {chatid}")
            conn.commit()
            return 'good'
    elif types == 'dream' or types == 'Dream' or types == 'dreams' or types == 'Dreams' or types == 'сон' or types == 'Сон':
        cursor.execute(f"SELECT limit_chat FROM config WHERE chat_id = {chatid}")
        row = cursor.fetchone()
        conn.commit()
        if row == None:
            cursor.execute(f"INSERT INTO config(chat_id, limit_dream) VALUES ({chatid}, {limit})")
            conn.commit()
            return 'good'
        else:
            cursor.execute(f"UPDATE config SET limit_dream = '{limit}' WHERE chat_id = {chatid}")
            conn.commit()
            return 'good'
    elif types == 'img' or types == 'Img' or types == 'image' or types == 'Image' or types == 'картинка' or types == 'изображение':
        cursor.execute(f"SELECT limit_img FROM config WHERE chat_id = {chatid}")
        row = cursor.fetchone()
        conn.commit()
        if row == None:
            cursor.execute(f"INSERT INTO config(chat_id, limit_img) VALUES ({chatid}, {limit})")
            conn.commit()
            return 'good'
        else:
            cursor.execute(f"UPDATE config SET limit_img = '{limit}' WHERE chat_id = {chatid}")
            conn.commit()
            return 'good'
    else:
        return 'bad'
    
def get_limit_dream(chatid):
    cursor.execute(f"SELECT limit_dream FROM config WHERE chat_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        cursor.execute(f"INSERT INTO config(chat_id) VALUES ({chatid})")
        conn.commit()
        return '350'
    else:
        return row[0]
    
def get_limit_img(chatid):
    cursor.execute(f"SELECT limit_img FROM config WHERE chat_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        cursor.execute(f"INSERT INTO config(chat_id) VALUES ({chatid})")
        conn.commit()
        return '60'
    else:
        return row[0]
        
def get_limit_chat(chatid):
    cursor.execute(f"SELECT limit_chat FROM config WHERE chat_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        cursor.execute(f"INSERT INTO config(chat_id) VALUES ({chatid})")
        conn.commit()
        return '320'
    else:
        return row[0]
        
def check_ban_chat(chatid):
    cursor.execute(f"SELECT ban FROM chats WHERE chat_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        cursor.execute(f"INSERT INTO chats(chat_id) VALUES ({chatid})")
        conn.commit()
        return '0'
    else:
        return row
     
def add_token(token):
    cursor.execute(f"INSERT INTO token(token) VALUES ('{token}')")
    conn.commit()
    
def receive_chats():
    cursor.execute(f"SELECT * FROM chats")
    row = cursor.fetchall()
    conn.commit()
    return row
     
def get_key():
    cursor.execute(f"SELECT token FROM token")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        return 'no key'
    else:
        return row[0]
        
def del_key(keys):
    cursor.execute(f"DELETE FROM token WHERE token = '{keys}'")
    conn.commit()
    
def check_adm(chatid):
    cursor.execute(f"SELECT level FROM admin WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        return '0'
    else:
        return row[0]
        
def add_moderator(chatid):
    cursor.execute(f"SELECT * FROM admin WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        cursor.execute(f"INSERT INTO admin(user_id) VALUES ({chatid})")
        conn.commit()
        return 'good'
    else:
        return 'already'
        
def del_moderator(chatid):
    cursor.execute(f"SELECT * FROM admin WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row == None:
        return 'bad'
    else:
        cursor.execute(f"DELETE FROM admin WHERE user_id = '{chatid}'")
        conn.commit()
        return 'good'
        
def ban(chatid):
    cursor.execute(f"SELECT level FROM admin WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row != None:
        return 'admin'
    cursor.execute(f"SELECT ban FROM users WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row[0] == '1':
        return 'already'
    if row == None:
        cursor.execute(f"SELECT ban FROM chats WHERE chat_id = {chatid}")
        row = cursor.fetchone()
        conn.commit()
        if row == None:
            return 'no user'
        if row[0] == '1':
            return 'already'
        else:
            cursor.execute(f"UPDATE chats SET ban = '1' WHERE chat_id = {chatid}")
            conn.commit()
            return 'good'
    else:
        cursor.execute(f"UPDATE users SET ban = '1' WHERE user_id = {chatid}")
        conn.commit()
        return 'good'
        
def unban(chatid):
    cursor.execute(f"SELECT level FROM admin WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row != None:
        return 'admin'
    cursor.execute(f"SELECT ban FROM users WHERE user_id = {chatid}")
    row = cursor.fetchone()
    conn.commit()
    if row[0] == '0':
        return 'already'
    if row == None:
        cursor.execute(f"SELECT ban FROM chats WHERE chat_id = {chatid}")
        row = cursor.fetchone()
        conn.commit()
        if row == None:
            return 'no user'
        if row[0] == '0':
            return 'already'
        else:
            cursor.execute(f"UPDATE chats SET ban = '0' WHERE chat_id = {chatid}")
            conn.commit()
            return 'good'
    else:
        cursor.execute(f"UPDATE users SET ban = '0' WHERE user_id = {chatid}")
        conn.commit()
        return 'good'
