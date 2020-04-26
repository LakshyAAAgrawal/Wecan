import mysql.connector
import time
from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__, static_url_path='/static')
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'wecan'
}

maxTries = 10
while True:
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        break
    except:
        print("Connection error")
        if maxTries > 0:
            time.sleep(2)
            maxTries = maxTries - 1
        else:
            exit(2)
            
@app.route('/')
def index():
    cursor.execute("SHOW DATABASES")
    return str(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug = True)
