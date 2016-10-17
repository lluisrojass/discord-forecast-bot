#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as s
from Errors import DatabaseException


class Database:

    def __init__(self, server_id: str):
        self.con = s.connect("Preference.db")
        self.cursor = None
        self.server_id = ''
        self._connect(server_id)

    def create_preference(self, user_name, user_id, location: str, is_metric=False):
        did_create = True
        # sql injection validation
        try:
            for word in location.split(' '):
                assert word.upper() not in ('SELECT', '*', 'ID', 'LOCATION', 'FROM', 'WHERE', 'UPDATE',
                                            'USER_ID', 'TIMES_REQUESTED', 'NAME', 'UNITS')
        except AssertionError:
                raise DatabaseException("Invalid location, preference not saved.")

        with self.con:
            # update if user already in server table
            if self._is_saved(user_id):
                self.cursor.execute("UPDATE {} SET location=? WHERE user_id=?;".format(self.server_id),
                                    (location, user_id))
                did_create = False
            # else, create preference
            else:
                self.cursor.execute("INSERT INTO {}(name,user_id, location, is_metric)"
                                    " VALUES (?,?,?,?);".format(self.server_id),
                                    (user_name, user_id, location, is_metric))
        return did_create

    def get_preference(self, user_id: str):
        with self.con:
            self.cursor.execute("SELECT location,is_metric FROM {} where user_id = ?;"
                                .format(self.server_id), (user_id,))
            data_tup = self.cursor.fetchone()
            if isinstance(data_tup, type(None)):
                raise DatabaseException("No results for user {}".format(user_id))
            return data_tup

    def _is_saved(self, user_id: str):
        with self.con:
            self.cursor.execute("SELECT user_id FROM {} where user_id = ?".format(self.server_id),
                                (user_id,))
            ans = self.cursor.fetchone()
            return user_id == ans[0] if not isinstance(ans, type(None)) else False

    def _connect(self, server_id):
        self.server_id = _encode(server_id)
        with self.con:
            self.cursor = self.con.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {}(Id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "name TEXT, "
                                "user_id TEXT,"
                                "location TEXT,"
                                "is_metric BOOLEAN);".format(self.server_id))

    def __del__(self):
        self.con.close()


def _encode(sid: str):
    base = 65  # utf U+0041 is char 'A' (65 decimal)
    out = ''
    for c in sid:
        if c.strip():
            char_from_glyph = chr(int(c) + base)  # highest possible value is U+0074 or 'J'
            out += char_from_glyph
    return out




