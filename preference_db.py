import sqlite3 as s
import sys


class Database:

    def __init__(self):
        self.con = s.connect("Preference.db")
        self.server_id = ""
        self.cursor = None

    def connect(self, server_id):
        self.server_id = server_id
        with self.con:
            self.cursor = self.con.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS ?(Id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "name TEXT, "
                                "user_id TEXT,"
                                "location TEXT,"
                                "times_requested INT)", (server_id, ))

    def create_preference(self, user_name, user_id, location):
        with self.con:
            times_requested = self.cursor.execute("SELECT times_requested FROM ? where user_id = ?",
                                                  (self.server, user_id))
            self.cursor.execute("INSERT INTO ?(name,user_id,"
                                "location,last_date_requested,times_requested) VALUES (?,?,?,?,?,?);",
                                (self.server_id, user_name, user_id, location, times_requested))

    def update(self, user_id, location):
        with self.con:
            self.cursor.execute("UPDATE ? SET location=? WHERE user_id=?", (self.server_id, location, user_id))

    def is_saved(self, user_id):
        with self.con:
            self.cursor.execute("SELECT user_id FROM ? where user_id = ?", (self.server_id, user_id))
            temp_user_id = self.cursor.fetchone()
            return user_id == temp_user_id

    def get_preference(self, user_id: str):
        with self.con:
            self.cursor.execute("SELECT location FROM ? where user_id = ?", (self.server_id, user_id))
            return self.cursor.fetchone()
        return None

    def __del__(self):
        self.con.close()
