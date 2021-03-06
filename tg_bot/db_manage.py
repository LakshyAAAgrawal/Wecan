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
dbConfig = dbConfig_docker
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
    "list_lists_of_user_board": 'SELECT list_id, list_name FROM LIST WHERE board_id="%s" AND ("%s", "%s") IN (SELECT user_id, board_id FROM BOARD_USER)',
    "check_list_with_username": 'SELECT 1 FROM LIST WHERE board_id="%s" AND list_name="%s" AND list_id="%s" AND ("%s", "%s") IN (SELECT user_id, board_id FROM BOARD_USER)',
    "get_list_name_by_id": "SELECT list_name FROM LIST WHERE list_id=\"%s\"",
    'list_cards_of_list': 'SELECT card_id, card_name FROM CARD WHERE list_id="%s" AND 1 IN (SELECT 1 FROM LIST WHERE list_id="%s" AND board_id="%s") AND 1 IN (SELECT 1 FROM BOARD_USER WHERE board_id="%s" AND user_id="%s")',
    "check_card_with_username": 'SELECT 1 FROM CARD WHERE card_id="%s" AND card_name="%s" AND list_id="%s" AND ("%s", "%s") IN (SELECT user_id, board_id FROM BOARD_USER) AND ("%s", "%s") IN (SELECT list_id, board_id FROM LIST)',
    'get_card_name_and_text_by_id': 'SELECT card_name, text FROM CARD where card_id="%s"',
    'get_card_comment_by_card_id': 'SELECT B.full_name, A.text FROM CARD_COMMENT AS A INNER JOIN USER AS B ON A.user_id=B.user_id WHERE A.card_id="%s"',
    'fetch_pending_deadlines': 'SELECT CARD.card_id, CARD.card_name, DEADLINE.due_date FROM DEADLINE, CARD, LIST, BOARD, BOARD_USER WHERE DEADLINE.due_date > CURTIME() AND DEADLINE.if_completed = FALSE AND DEADLINE.card_id = CARD.card_id AND CARD.list_id = LIST.list_id AND LIST.board_id = BOARD.board_id AND BOARD.board_id = BOARD_USER.board_id AND BOARD_USER.user_id="%s"',
    "add_comment": 'INSERT INTO CARD_COMMENT(card_id, user_id, text) VALUES ("%s", "%s", "%s")',
    "create_card": 'INSERT INTO CARD(list_id, card_admin, card_name, text, multimedia_id) VALUES ("%s", "%s", "%s", "%s", "%s")'
}

def add_comment_db(comment_text, card_id, username):
    try:
        conn = mysql.connector.connect(**dbConfig)
        conn.autocommit = False
        cur = conn.cursor()
        print(queries['add_comment'] % (card_id, username, comment_text))
        cur.execute(queries['add_comment'] % (card_id, username, comment_text))
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

def fetch_pending_deadlines(username):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['fetch_pending_deadlines'] % (username))
    return cursor.fetchall()

def fetch_card(card_id):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['get_card_name_and_text_by_id'] % (card_id))
    card_name, card_text = cursor.fetchone()
    cursor.execute(queries['get_card_comment_by_card_id'] % (card_id))
    comments = cursor.fetchall()
    return card_name, card_text, comments

def fetch_card_name(card_id):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['get_card_name_and_text_by_id'] % (card_id))
    card_name, card_text = cursor.fetchone()
    return card_name

def get_board_name_by_id(board_id):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['get_board_name_by_id'] % (board_id))
    z = cursor.fetchone()
    if z is not None:
        return z[0]
    else:
        raise Exception

def get_list_name_by_id(list_id):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['get_list_name_by_id'] % (list_id))
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

def check_list_exists(board_id, username, list_name, list_id):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['check_list_with_username'] % (board_id, list_name, list_id, username, board_id))
    z = cursor.fetchone()
    return True if z != None else False

def check_card_exists(username, board_id, list_id, card_id, card_name):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['check_card_with_username'] % (card_id, card_name, list_id, username, board_id, list_id, board_id))
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

def create_card_in_db(list_id, username, card_name, card_content, multimedia_id):
    try:
        conn = mysql.connector.connect(**dbConfig)
        conn.autocommit = False
        cur = conn.cursor()
        print(queries["create_card"] % (list_id, username, card_name, card_content, multimedia_id))
        cur.execute(queries["create_card"] % (list_id, username, card_name, card_content, multimedia_id))
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

def fetch_cards_of(username, board_id, list_id):
    connect()
    cursor = connection.cursor()
    cursor.execute(queries['list_cards_of_list'] % (list_id, list_id, board_id, board_id, username))
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
                time.sleep(10)
                maxTries = maxTries - 1
            else:
                exit(2)

connect()
