#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as s
import sys
import discord


class Database:

    def __init__(self):
        self.con = s.connect("Preference.db")
        self.cursor = None
        self.server_id = None

    def _connect(self, server_id):
        self.server_id = _encode(server_id)
        with self.con:
            self.cursor = self.con.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {}(Id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "name TEXT, "
                                "user_id TEXT,"
                                "location TEXT,"
                                "times_requested INT)".format(self.server_id))

    def create_preference(self, ctx, location: str):
        self._connect(ctx.message.server.id)
        with self.con:
            if self.is_saved(ctx.message.author.id) is True:  # update location
                self.cursor.execute("UPDATE {} SET location=? WHERE user_id=?".format(self.server_id),
                                    (location, ctx.message.author.id))
                return False
            else:  # create preference
                self.cursor.execute("INSERT INTO {}(name,user_id, location) VALUES (?,?,?);".format(self.server_id),
                                    (ctx.message.author.name, ctx.message.author.id, location))
                self.cursor.execute("UPDATE {} SET times_requested = times_requested + 1 WHERE user_id = ?"
                                    .format(self.server_id), (ctx.message.author.id,))
                return True

    def is_saved(self, user_id):
        with self.con:
            self.cursor.execute("SELECT user_id FROM {} where user_id = ?".format(self.server_id),
                                (user_id,))
            temp_user_id = self.cursor.fetchone()
            return user_id == temp_user_id

    def get_preference(self, user_id: str):
        with self.con:
            self.cursor.execute("SELECT location FROM {} where user_id = ?"
                                .format(self.server_id), (user_id,))
            return self.cursor.fetchone()

    def __del__(self):
        self.con.close()


def _encode(l: str):
    out = ''
    for c in l:
        char_from_glyph = chr(int(c) + 65)
        out += char_from_glyph
    return out
