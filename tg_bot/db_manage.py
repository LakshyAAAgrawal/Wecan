import time
import mysql.connector
from mysql.connector import Error

dbConfig_local = {
    'user': 'bot',
    'password': 'password',
    #'host': 'db',
    'host': '127.0.0.1',
    #'port': '3306',
    'port': '32000',
    'database': 'wecan'
}
dbConfig_docker = {
    'user': 'bot',
    'password': 'password',
    'host': 'db',
    #'host': '127.0.0.1',
    'port': '3306',
    #'port': '32000',
    'database': 'wecan'
}
dbConfig = dbConfig_local
connection = None
cursor = None

queries = {
    "check_username": "SELECT 1 FROM USERS WHERE id=\"%s\"",
    "check_login": "SELECT 1 FROM USERS WHERE id=\"%s\" AND password=\"%s\"",
    "list_boards_of_user_where": 'SELECT id, name FROM BOARDS WHERE id IN (SELECT board_id FROM BOARD_USERS WHERE user_id="%s" AND board_id="%s")', # 1.935 sec
    "list_boards_of_user_join": 'SELECT A.id, A.name FROM BOARDS AS A INNER JOIN BOARD_USERS AS B ON A.id=B.board_id WHERE B.user_id="%s"', # 0.072 sec
    "create_board": 'INSERT INTO BOARDS(name, admin_id) VALUES (%s, %s)', # TODO - remove organisation id
    "add_user_to_board": 'INSERT INTO BOARD_USERS(user_id, board_id) VALUES (%s, %s)',
}

def check_username_exists(username):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['check_username'] % (username))
    z = cursor.fetchone()
    print(z)
    return True if z != None else False

def create_board_in_db(username, board_name):
    try:
        conn = mysql.connector.connect(**dbConfig)
        conn.autocommit = False
        cur = conn.cursor()
        print(queries["create_board"] % (board_name, username))
        cur.execute(queries["create_board"], (board_name, username))
        board_id = cur.lastrowid
        print(queries["add_user_to_board"] % (username, board_id))
        cur.execute(queries["add_user_to_board"], (username, board_id))
        conn.commit()
        return True
    except mysql.connector.Error as error :
        print("Failed to update record to database rollback: {}".format(error))
        conn.rollback()
        return False
    except Exception as error2:
        print("Some other error: {}".format(error2))
        return False
    finally:
        if(conn.is_connected()):
            if cur is not None:
                cur.close()
            conn.close()
    return False
                
def fetch_boards_of(username):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['list_boards_of_user_join'] % (username))
    return cursor.fetchall()
                
def check_login(username, password):
    connect()
    cursor = connection.cursor()
    print(queries["check_login"] % (username, password))
    cursor.execute(queries["check_login"] % (username, password))
    z = cursor.fetchone()
    print(z)
    return True if z != None else False

def connect():
    global connection, cursor
    maxTries = 20
    while True:
        try:
            connection = mysql.connector.connect(**dbConfig)
            cursor = connection.cursor()
            print("Connected")
            break
        except:
            print("Connection error")
            if maxTries > 0:
                time.sleep(2)
                maxTries = maxTries - 1
            else:
                exit(2)

connect()
