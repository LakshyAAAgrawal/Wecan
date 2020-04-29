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
    "check_username": "SELECT 1 FROM USER WHERE user_id=\"%s\"",
    "check_login": "SELECT 1 FROM USER WHERE user_id=\"%s\" AND passwd=\"%s\"",
    "list_boards_of_user_where": 'SELECT board_id, board_name FROM BOARD WHERE board_id IN (SELECT board_id FROM BOARD_USER WHERE user_id="%s" AND board_id="%s")', # 1.935 sec
    "list_boards_of_user_join": 'SELECT A.board_id, A.board_name FROM BOARD AS A INNER JOIN BOARD_USER AS B ON A.board_id=B.board_id WHERE B.user_id="%s"', # 0.072 sec
    "create_board": 'INSERT INTO BOARD(board_name, board_admin) VALUES (%s, %s)', # TODO - remove organisation id
    "add_user_to_board": 'INSERT INTO BOARD_USER(user_id, board_id) VALUES (%s, %s)',
    "check_board_without_username": "SELECT 1 FROM BOARD WHERE board_name=\"%s\" AND board_id=\"%s\"", # Less performant
    "check_board_with_username": 'SELECT 1 FROM BOARD AS A INNER JOIN BOARD_USER AS B ON A.board_id=B.board_id WHERE A.board_id="%s" AND A.board_name="%s" AND B.user_id="%s"', # more performant
    "get_board_name_by_id": "SELECT board_name FROM BOARD WHERE board_id=\"%s\"",
    "create_list": 'INSERT INTO LIST(board_id, list_name, list_admin, list_label) VALUES ("%s", "%s", "%s", "%s")',
    "list_lists_of_user_board": 'SELECT list_id, list_name FROM LIST WHERE board_id="%s" AND ("%s", "%s") IN (SELECT user_id, board_id FROM BOARD_USER);'
}

def get_board_name_by_id(board_id):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['get_board_name_by_id'] % (board_id))
    z = cursor.fetchone()
    if z is not None:
        return z[0]
    else:
        raise Exception

def check_board_exists(board_name, board_id, username):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['check_board_with_username'] % (board_id, board_name, username))
    z = cursor.fetchone()
    return True if z != None else False

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

def create_list_in_db(username, board_id, list_name, label):
    try:
        conn = mysql.connector.connect(**dbConfig)
        conn.autocommit = False
        cur = conn.cursor()
        print(queries["create_list"] % (board_id, list_name, username, label))
        cur.execute(queries["create_list"] % (board_id, list_name, username, label))
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

def fetch_lists_of(board_id, username):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['list_lists_of_user_board'] % (board_id, username, board_id))
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
