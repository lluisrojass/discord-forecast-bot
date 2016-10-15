#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as s


class Database:

    def __init__(self):
        self.con = s.connect("Preference.db")
        self.cursor = None
        self.server_id = ''
        self.is_connected = None

    def create_preference(self, user_name, user_id, location: str):
        # simple sql injection validation
        try:
            for word in location.split(' '):
                assert word.upper() not in ('SELECT', '*', 'ID', 'LOCATION', 'FROM', 'WHERE', 'UPDATE',
                                            'USER_ID', 'TIMES_REQUESTED', 'NAME')
        except AssertionError:
                return 0
        # ensure connection
        if self.is_connected:
            with self.con:
                # update if user already in server table
                if self._is_saved(user_id) is True:
                    self.cursor.execute("UPDATE {} SET location=? WHERE user_id=?".format(self.server_id),
                                        (location, user_id))
                    return 1
                # else, create preference
                else:
                    self.cursor.execute("INSERT INTO {}(name,user_id, location, times_requested)"
                                        " VALUES (?,?,?,1);".format(self.server_id),
                                        (user_name, user_id, location))
                    self.cursor.execute("UPDATE {} SET times_requested = times_requested + 1 WHERE user_id = ?"
                                        .format(self.server_id), (user_id,))
                    return 2
        else:
            return 3

    def get_preference(self, user_id: str):
        with self.con:
            self.cursor.execute("SELECT location FROM {} where user_id = ?"
                                .format(self.server_id), (user_id,))
            return self.cursor.fetchone()

    def _is_saved(self, user_id: str):
        with self.con:
            self.cursor.execute("SELECT user_id FROM {} where user_id = ?".format(self.server_id),
                                (user_id,))
            return user_id == self.cursor.fetchone()[0]

    def connect(self, server_id):
        self.server_id = _encode(server_id)
        if len(self.server_id) is 0:
            return False
        with self.con:
            self.cursor = self.con.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {}(Id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "name TEXT, "
                                "user_id TEXT,"
                                "location TEXT,"
                                "times_requested INT)".format(self.server_id))
            return True

    def __del__(self):
        self.con.close()


def _encode(sid: str):
    try:
        base = 65  # utf U+0041 is char 'A' (65 decimal)
        out = ''
        for c in sid:
            char_from_glyph = chr(int(c) + base)  # highest possible value is U+0074 or 'J'
            out += char_from_glyph
        return out
    except Exception:
        return ''




