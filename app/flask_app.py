import mysql
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
    except mysql.connector.errors.InterfaceError:
        if maxTries > 0:
            time.sleep(2)
            maxTries = maxTries - 1
        else:
            exit("MySql Connection error")
            
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug = True)
