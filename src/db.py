#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as s

DB_NAME = '../db/4CAST.db'

class DatabaseException(Exception):
    def __init__(self, message):
        super(DatabaseException, self).__init__(message)

def __validate(location):
    for word in location.split(' '):
                assert word.upper() not in ('SELECT', '*', 'ID', 'LOCATION', 'FROM', 'WHERE', 'UPDATE',
                                            'USER_ID', 'TIMES_REQUESTED', 'NAME', 'UNITS')

def add_preference(location, is_metric, name, user_id):
    con = s.connect(DB_NAME)
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pref(Id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, user_id TEXT, location TEXT, is_metric BOOLEAN);")
    try:
        __validate(location)
    except AssertionError:
        raise DatabaseException('Bad Location Identifier, preference not saved.')

    with con:
        cursor.execute("SELECT user_id FROM pref where user_id = ?", (user_id,))
        reply = cursor.fetchone()
        exists = True if not isinstance(reply, type(None)) else False
        if exists:
            cursor.execute("UPDATE pref SET location=?,is_metric=? WHERE user_id=?",(location, is_metric, user_id))
        else:
            cursor.execute("INSERT INTO pref (location, is_metric, name, user_id) VALUES(?,?,?,?)",(location, is_metric, name, user_id))

    return not exists

def get_preference(user_id):
    con = s.connect(DB_NAME)
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pref(Id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, user_id TEXT, location TEXT, is_metric BOOLEAN);")
    with con:
        cursor.execute("SELECT location,is_metric FROM pref WHERE user_id=?",(user_id,))
        reply = cursor.fetchone()
        if isinstance(reply, type(None)):
            raise DatabaseException('No Weather Preference found.')
        else:
            return reply