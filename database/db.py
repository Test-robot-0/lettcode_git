import sqlite3
import config

def getConnection():
    return sqlite3.connect(config.DATABASE)
