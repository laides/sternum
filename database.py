import sqlite3
import os


DATABASE = 'server.db'

class DataBase():
    def __init__(self):
        if os.path.isfile(DATABASE):
            os.remove(DATABASE)

        self.conn = sqlite3.connect(DATABASE)
        self.c = self.conn.cursor()

    def create_database(self):
        # initiate the db, connect and create the table
        self.conn.text_factory = bytes
        try:
            self.c.executescript("""CREATE TABLE parking_visitors(plate_number text NOT NULL PRIMARY KEY,
                                decision text, 
                                timestamp text,
                                car_type text);
                            """)
            self.conn.commit()
        except:
            print("table already created - if this is not the first run, ignore this msg.")

    def insert(self,license_number,allowed,timestamp,car_type):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO parking_visitors VALUES (?,?,?,?)",
                                  (license_number, allowed, str(timestamp),car_type))
                self.conn.commit()
        except Exception as e:
            print("RETURN HERE ERROR 9000 - Insert "+license_number + ','+e.message)

    def get_all_visitors(self):
        try:
            with self.conn:
                self.c.execute("SELECT * FROM parking_visitors")
                visitors_list = self.c.fetchall()
            return visitors_list
        except:
            print("RETURN HERE ERROR 9000 - get_all_visitors")

    def close(self):
        # close database connection
        self.conn.close()

