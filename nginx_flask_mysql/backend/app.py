import os
from flask import Flask
import mysql.connector

class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(user='root', host='db', database='example', password='test-123n')
        #self.connection = mysql.connector.connect(
        #    user=user,
        #    password=pf.read(),
        #    host=host, # name of the mysql service as set in the docker compose file
        #    database=database
        #)
        pf.close()
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
        self.connection.commit()

    def query_titles(self):
        self.cursor.execute('SELECT title FROM blog')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


server = Flask(__name__)
db_mng = None

@server.route('/')
def listBlog():
    global db_mng
    if not db_mng:
        db_mng = DBManager(password_file='/run/secrets/db-password')
        db_mng.populate_db()
    rec = db_mng.query_titles()

    response = ''
    for c in rec:
        response = response  + '<div>   Hello  ' + c + '</div>'
    return response


if __name__ == '__main__':
    server.run()
