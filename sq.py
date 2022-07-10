import sqlite3
from getpass import getuser

with sqlite3.connect(f"/home/{getuser()}/main.sqlite") as con:

    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login STRING NOT NULL,
    email String NOT NULL,
    password String NOT NULL,
    time_registration String NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS News (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login STRING NOT NULL,
    time  STRING NOT NULL,
    seo_title STRING,
    seo_description STRING,
    title STRING NOT NULL,
    subtitle STRING,
    content_page STRING,
    short_link STRING,
    img STRING,
    is_deleted INTEGER NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Tag_news(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login STRING NOT NULL,
    time  STRING NOT NULL,
    title STRING NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS User_auth_log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time STRING NOT NULL,
    login STRING NOT NULL
    )""")
