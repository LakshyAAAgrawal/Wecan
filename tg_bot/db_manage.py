import time
import mysql.connector
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
    "list_boards_of_user_join": 'SELECT A.id, A.name FROM BOARDS AS A INNER JOIN BOARD_USERS AS B ON A.id=B.board_id WHERE B.user_id="%s"' # 0.072 sec
}

def check_username_exists(username):
    cursor.execute(queries['check_username'] % (username))
    z = cursor.fetchone()
    print(z)
    return True if z != None else False

def fetch_boards_of(username):
    cursor.execute(queries['list_boards_of_user_join'] % (username))
    return cursor.fetchall()    

def check_login(username, password):
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
