import sqlite3
from sqlite3 import Error
from flask import Flask, request, jsonify
from flask_cors import CORS

def connect_to_db():
    conn = sqlite3.connect('test.db')
    return conn

def create_db():
    """ create a database connection to a SQLite database """
    try:
        conn = connect_to_db()
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS websites (
                        user_id INTEGER PRIMARY KEY NOT NULL,
                        category TEXT NOT NULL,
                        url TEXT NOT NULL
                    );
        ''')
        conn.commit()
        print("User table created successfully")
    except Error as e:
        print(e)
    finally:
        conn.close()

def insert_data(website):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        data = ( website["category"], website["url"])
        sqlite_param = '''
                    INSERT INTO websites (
                        category, url
                    )
                    VALUES (
                        ?, ?
                    )
        '''
        cur.execute(sqlite_param, data)
        conn.commit()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        conn.close()

def get_websites():
    websites = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM websites")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            website = {}
            website["user_id"] = i["user_id"]
            website["category"] = i["category"]
            website["url"] = i["url"]
            websites.append(website)

    except:
        websites = []

    return websites

web = []
web0 = {
    "category": "test",
    "url": "google.com"
}
web1 = {
"category": "test",
"url": "youtube.com"
}
web2 = {
    "category": "test",
    "url": "twitter.com"
}
web.append(web0)
web.append(web1)
web.append(web2)
create_db()
for i in web:
    insert_data(i)



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/websites', methods=['GET'])
def page_get_websites():
    return jsonify(get_websites())
if __name__ == '__main__':
    app.run(debug = True)

