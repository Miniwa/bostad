"""
Storage.
"""
import sqlite3


class Storage():
    """
    SQLite based storage.
    """
    @classmethod
    def create_or_open(cls, filename):
        return Storage(sqlite3.connect(filename))

    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()
        self.create_tables()

    def create_tables(self):
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS Housing(
            Address TEXT
        )""")

    def has_address(self, address):
        return self.get_address(address) is not None


    def get_address(self, address):
        self._cursor.execute("SELECT * FROM Housing WHERE Address = ?", (address,))
        return self._cursor.fetchone()

    def insert_address(self, address):
        if self.has_address(address):
            raise ValueError("Duplicate entries are not allowed.")

        self._cursor.execute("""INSERT INTO Housing VALUES (?)""", (address,))
        self._conn.commit()
