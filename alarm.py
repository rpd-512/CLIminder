import os
import sqlite3
from notifypy import Notify #if not available, install with "pip3 install notify-py"
from time import sleep
from datetime import datetime, date, timedelta
loc = str(os.path.dirname(__file__))
dbPath = loc+"/database/database.db"
conn = sqlite3.connect(dbPath)

wk = ["monday", "teusday", "wednesday", "thursday", "friday", "saturday", "sunday"]
notify = Notify()

try:
    os.system("clear")
except:
    os.system("cls")


def remind(time,date,desc,id):
    cursor = conn.execute("select sound from alarm_data")
    for i in cursor:
        if(i[0] == "e"):
            notify.audio = loc+"/audio/sound.wav"
    ttle = "A Reminder | "+time+" | "+date
    notify.title = ttle
    notify.message = desc
    notify.icon = loc+"/icon/icon.png"
    notify.send()
    if(id != None):
        conn.execute("update reminders set done = 1 where rmid = "+str(id))
        conn.commit()
tmsecs = 0

while(True):

    tmsecs += 1
    sleep(1)
    try:
        os.system("clear")
    except:
        os.system("cls")
    nw = datetime.now()
    exc = "select * from reminders where done = 0"
    cursor = conn.execute(exc)
    for i in cursor:
        desc = str(i[1])
        hr = str(i[2])
        mn = str(i[3])
        rpt = str(i[4])
        d = str(i[5])
        m = str(i[6])
        y = str(i[7])
        dly = str(i[8])
        if(int(dly) != 0 and tmsecs%int(dly) == 0):
            remind("in delay of "+str(int(int(dly)/60))+" minutes","",desc,None)
        try:
            tm = datetime.strptime(d+"/"+m+"/"+y+" "+hr+":"+mn+":00", "%d/%m/%Y %H:%M:%S")
            if(tm < nw):
                if(rpt != ""):
                    if(rpt == "y"):
                        conn.execute("update reminders set year = "+str(nw.year+1)+" where rmid = "+str(i[0]))
                        conn.commit()
                        remind(hr+":"+mn,d+"-"+m+" (Every year)",desc,None)
                    elif(rpt == "d"):
                        remind(hr+":"+mn,"(Every day)",desc,None)
                        tm = date.today() + timedelta(days = 1)
                        d = str(tm.strftime("%d"))
                        m = str(tm.strftime("%m"))
                        y = str(tm.strftime("%Y"))
                        conn.execute("update reminders set date = "+d+", mnth = "+m+", year = "+y+" where rmid = "+str(i[0]))
                        conn.commit()
                    elif(rpt == "w"):
                        remind(hr+":"+mn,"(Every "+str(wk[i[10]])+")",desc,None)
                        tm = date.today() + timedelta(days = 7)
                        d = str(tm.strftime("%d"))
                        m = str(tm.strftime("%m"))
                        y = str(tm.strftime("%Y"))
                        conn.execute("update reminders set date = "+d+", mnth = "+m+", year = "+y+" where rmid = "+str(i[0]))
                        conn.commit()
                    elif(rpt == "c"):
                        remind(hr+":"+mn,"(Every "+str(i[11])+" days)",desc,None)
                        tm = date.today() + timedelta(days = i[11])
                        d = str(tm.strftime("%d"))
                        m = str(tm.strftime("%m"))
                        y = str(tm.strftime("%Y"))
                        conn.execute("update reminders set date = "+d+", mnth = "+m+", year = "+y+" where rmid = "+str(i[0]))
                        conn.commit()
                    elif(rpt == "m"):
                        remind(hr+":"+mn,"(Every "+str(wk[i[10]])+")",desc,None)
                        tm = date.today() + timedelta(days = 30)
                        d = str(tm.strftime("%d"))
                        m = str(tm.strftime("%m"))
                        y = str(tm.strftime("%Y"))
                        conn.execute("update reminders set date = "+d+", mnth = "+m+", year = "+y+" where rmid = "+str(i[0]))
                        conn.commit()
                elif(rpt == ""):
                    remind(hr+":"+mn,d+"-"+m+"-"+y,desc,i[0])
        except:
            pass
