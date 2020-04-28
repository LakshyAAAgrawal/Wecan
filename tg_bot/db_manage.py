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
    "check_username": "SELECT 1 FROM USERS WHERE id=%s",
    "check_login": "SELECT 1 FROM USERS WHERE id=%s AND password=\"%s\""
}

def check_username_exists(username):
    cursor.execute(queries['check_username'] % (username))
    z = cursor.fetchone()
    return True if type(z) != None else False

def check_login(username, password):
    cursor.execute(queries["check_login"] % (username, password))
    z = cursor.fetchone()
    return True if type(z) != None else False

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
