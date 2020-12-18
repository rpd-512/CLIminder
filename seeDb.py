import sqlite3
import os
import time
dbPath = str(os.path.dirname(__file__))
dbPath = dbPath+"/database/database.db"
conn = sqlite3.connect(dbPath)
while(True):
    cursor = conn.execute("SELECT * from reminders")
    for row in cursor:
        print(row)
    time.sleep(0.5)
    os.system("clear")
conn.close()