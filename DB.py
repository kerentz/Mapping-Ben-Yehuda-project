import sqlite3

conn = sqlite3.connect('test.db', check_same_thread=False)

conn.execute('''CREATE TABLE IF NOT EXISTS USERS(
         ID integer PRIMARY KEY AUTOINCREMENT,
         EMAIL               TEXT    NOT NULL,
         PASSWORD            TEXT     NOT NULL);''')


def register(email, password):
    conn.execute('''INSERT INTO USERS(EMAIL,PASSWORD) VALUES("%s","%s")''' % (email, password))


def login(email, password):
    known_password = conn.execute('''SELECT PASSWORD FROM USERS where EMAIL="%s"''' % email)
    if password == known_password.fetchone()[0]:
        return 'yes'
    return 'no'
