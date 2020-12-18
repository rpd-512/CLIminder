import sqlite3
import os
import datetime
from texttable import Texttable
from time import sleep
dbPath = os.getcwd()
try:
    os.mkdir(dbPath+"/database")
except:
    pass
dbPath = dbPath+"/database/database.db"
conn = sqlite3.connect(dbPath)
try:
    conn.execute("""create table reminders(
        rmid integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        desc text,
        hrs integer,
        mnt integer,
        rpt text,
        date integer,
        mnth integer,
        year integer,
        dly integer,
        wkdy integer,
        done integer,
        days integer
    )""")
    conn.execute("""create table alarm_data(
        sound varchar(1)
        )""")
    conn.execute("insert into alarm_data values ('e')")
    conn.commit()
except:
    pass
if(os.name == 'nt'):
    clrscr = "cls"
else:
    clrscr = "clear"

hlp = """\n|HELP|
            -> ent   - new entry
            -> show  - shows all entries
            -> dlt   - deletes an entry (use: "dlt id" where id is the entry id.. get entry id's by using show command)
            -> clear - clear screen
            -> exit  - exit program
            -> reset - resets everything, i.e. deletes all reminders.
            -> snd   - toggle sound in reminder
            -> \\h    - help
            -> \\a    - about\n"""
abt = """\n|ABOUT|
            This is a CLI, python based reminder application created by Rhiddhi Prasad Das.
            Github : https://github.com/rpd-512/
            Twitter: https://twitter.com/RhiddhiD
            Fiverr : https://www.fiverr.com/rpd_512
            Email  : rhiddhiprasad@gmail.com\n"""
os.system(clrscr)
def valiDate(date_text):
    datetime.datetime.strptime(date_text, '%Y-%m-%d')
def validatime(h,m):
    datetime.datetime.strptime(str(h)+":"+str(m)+":00","%H:%M:%S")
def ftrpst(d,m,y,hr,mn):
    d, m, y, hr, mn = str(d), str(m), str(y), str(hr), str(mn)
    prsnt = datetime.datetime.now()
    gvntm = datetime.datetime.strptime(d+"/"+m+"/"+y+" "+hr+":"+mn+":00", "%d/%m/%Y %H:%M:%S")
    if(prsnt < gvntm):
        return True
    else:
        return False
def entry():
    desc,hr,mn,rpt,dte,mnt,yer,dly,wkdy,dys = "",0,0,"",0,0,0,0,0,0
    wk = ["monday", "teusday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    print("\nNew entry (Press ctrl+c to cancel)\n")
    try:
        desc = input("Enter description: ")
        while(True):
            rmnd = input("Remind at specific (T)ime or in a (D)elay ?: ").lower()
            if(rmnd != "t" and rmnd != "d"):
                print("! invalid input !")
                continue
            break
        if(rmnd == "t"):
            evdy = input("Remind: \n-> every (d)ay, \n-> every (w)eek, \n-> every (m)onth, \n-> every (y)ear or\n-> (c)ustom (leave blank for no repeat): ").lower()
            if(evdy != "d" and evdy != "w" and evdy != "m" and evdy != "y" and evdy != "c"):
                print("No Repeat selected")
                while(True):
                    while(True):
                        try:
                            tm = input("Enter time (in 24 hour format like hh:mm): ")
                            hr = int(tm.split(":")[0])
                            mn = int(tm.split(":")[1])
                            validatime(hr,mn)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid time !\n")
                            continue
                    while(True):
                        try:
                            date = input("Enter date (in the following format: dd/mm/yyyy): ")
                            dte = date.split("/")[0]
                            mnt = date.split("/")[1]
                            yer = date.split("/")[2]
                            valiDate(yer+"-"+mnt+"-"+dte)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid date !\n")
                            continue
                    if(ftrpst(dte,mnt,yer,hr,mn)):
                        break
                    else:
                        print("\n! Error, the time you entered seems to be in the past, please re-check !\n")
                        continue

            elif(evdy == "d"):
                print("Repeat every day")
                rpt = 'd'
                while(True):
                    try:
                        tm = input("Enter time (in 24 hour format like hh:mm): ")
                        hr = int(tm.split(":")[0])
                        mn = int(tm.split(":")[1])
                        validatime(hr,mn)
                        dte = datetime.date.today().strftime("%d")
                        mnt = datetime.datetime.now().month
                        yer = datetime.datetime.now().year
                        print(dte,mnt,yer)
                        break
                    except(KeyboardInterrupt):
                        print("\n|CANCELLED|")
                        return 0
                    except:
                        print("! invalid time !\n")
                        continue
                print("Reminder set for everyday :)")
            elif(evdy == "w"):
                rpt = "w"
                print("Repeat every week")
                while(True):
                    try:
                        tm = input("Enter time (in 24 hour format like hh:mm): ")
                        hr = int(tm.split(":")[0])
                        mn = int(tm.split(":")[1])
                        validatime(hr,mn)
                        break
                    except(KeyboardInterrupt):
                        print("\n|CANCELLED|")
                        return 0
                    except:
                        print("! invalid time !\n")
                        continue
                while(True):
                    try:
                        wkdy = int(input("Enter the week day number (monday is 1): "))
                        if(wkdy < 1 or wkdy >7):
                            raise "error day"
                        else:
                            print("The reminder is set for "+str(wk[wkdy-1])+" every week")
                            break
                    except (KeyboardInterrupt):
                        return 0
                    except:
                        print("! invalid input !, (monday = 1, teusday = 2, wednesday = 3, thursday = 4, friday = 5, saturday = 6, sunday = 7)")
                dt = datetime.date.today()
                for i in range(7):
                    if(dt.weekday()+1 == wkdy):
                        break
                    dt = dt + datetime.timedelta(days = 1)
                dte = dt.strftime("%d")
                mnt = dt.strftime("%m")
                yer = dt.strftime("%Y")
            elif(evdy == "m"):
                rpt = "m"
                print("Repeat every month (30 days)")
                while(True):
                    while(True):
                        try:
                            tm = input("Enter time (in 24 hour format like hh:mm): ")
                            hr = int(tm.split(":")[0])
                            mn = int(tm.split(":")[1])
                            validatime(hr,mn)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid time !\n")
                            continue
                    while(True):
                        try:
                            date = input("Enter starting date (in the following format: dd/mm/yyyy): ")
                            dte = date.split("/")[0]
                            mnt = date.split("/")[1]
                            yer = date.split("/")[2]
                            valiDate(yer+"-"+mnt+"-"+dte)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid date !\n")
                            continue
                    if(ftrpst(dte,mnt,yer,hr,mn)):
                        break
                    else:
                        print("\n! Error, the time you entered seems to be in the past, please re-check !\n")
                        continue
                
            elif(evdy == "y"):
                print("Repeat every year")
                rpt = "y"
                while(True):
                    while(True):
                        try:
                            tm = input("Enter time (in 24 hour format like hh:mm): ")
                            hr = int(tm.split(":")[0])
                            mn = int(tm.split(":")[1])
                            validatime(hr,mn)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid time !\n")
                            continue
                    while(True):
                        try:
                            date = input("Enter date (in the following format: dd/mm): ")
                            dte = date.split("/")[0]
                            mnt = date.split("/")[1]
                            yer = datetime.date.today().strftime("%Y")
                            valiDate(yer+"-"+mnt+"-"+dte)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid date !\n")
                            continue
                    if(ftrpst(dte,mnt,yer,hr,mn)):
                        break
                    else:
                        yer = int(yer)+1
                        break
            elif(evdy == "c"):
                rpt = 'c'
                print("Custom")
                while(True):
                    while(True):
                        try:
                            tm = input("Enter time (in 24 hour format like hh:mm): ")
                            hr = int(tm.split(":")[0])
                            mn = int(tm.split(":")[1])
                            validatime(hr,mn)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid time !\n")
                            continue
                    while(True):
                        try:
                            date = input("Enter starting date (in the following format: dd/mm/yyyy): ")
                            dte = date.split("/")[0]
                            mnt = date.split("/")[1]
                            yer = date.split("/")[2]
                            valiDate(yer+"-"+mnt+"-"+dte)
                            break
                        except(KeyboardInterrupt):
                            print("\n|CANCELLED|")
                            return 0
                        except:
                            print("! invalid date !\n")
                            continue
                    if(ftrpst(dte,mnt,yer,hr,mn)):
                        break
                    else:
                        print("\n! Error, the time you entered seems to be in the past, please re-check !\n")
                        continue
                try:
                    dys = int(input("Enter number of days for delay: "))
                    if(dys < 1):
                        raise ("bad delay")
                except(KeyboardInterrupt):
                    print("\n|CANCELLED|")
                    return 0
                except:
                    print("! invalid input ! the delay should be an integer and greater than 0")

        elif(rmnd == "d"):
            while(True):
                try:
                    dly = int(input("Enter your delay in minutes: "))*60
                    if(dly < 1):
                        raise ValueError("bad delay")
                    break
                except:
                    print("! invalid input ! the delay should be an integer and greater than 0")
        cmnd = "insert into reminders (desc, hrs, mnt, rpt, date, mnth, year, dly,  wkdy, done, days) values ('"+str(desc)+"',"+str(hr)+","+str(mn)+",'"+str(rpt)+"',"+str(dte)+","+str(mnt)+","+str(yer)+","+str(dly)+","+str(wkdy)+",0,"+str(dys)+");"
        conn.execute(cmnd)
        conn.commit()
        print("Reminder set :)")
    except(KeyboardInterrupt):
        print("\n|CANCELLED|\n")
        pass

def show_all():
    cursor = conn.execute("SELECT * from reminders")
    t = Texttable()
    t.set_cols_align(['c','c','c','c','c','c','c'])
    t.header(["Id","Description","Time","Repeat","Scheduled Date","Delay","Occurred"])
    for row in cursor:
        id = row[0]
        desc = row[1]
        time = str(row[2])+":"+str(row[3])
        rpt = row[4]
        date = str(row[5])+"-"+str(row[6])+"-"+str(row[7])
        dly = int(row[8]/60)
        ocr = "-"
        if(rpt == "d"):
            rpt = "Every day"
        if(rpt == "w"):
            rpt = "Every week"
        if(rpt == "y"):
            rpt = "Every year"
        if(rpt == "m"):
            rpt = "Every month"
        if(rpt == "c"):
            rpt = "Every "+str(row[11])+" days"
        if(rpt == ''):
            rpt = "-"
        if(dly != 0):
            time = "-"
            date = "-"
            dly = str(dly)+" minutes"
        else:
            dly = "-"
        if(row[10] == 1 and rpt == "-" and dly == 0):
            ocr = "Yes"
        elif(row[10] == 0 and rpt == "-" and dly == 0):
            ocr = "No"
        t.add_row([id,desc,time,rpt,date,dly,ocr])
    print(t.draw())

def dlt(id):
    cursor = conn.execute("SELECT * from reminders where rmid = "+str(id))
    t = Texttable()
    t.set_cols_align(['c','c','c','c','c','c'])
    t.header(["Id","Description","Time","Repeat","Scheduled Date","Delay"])
    navlb = True
    for row in cursor:
        navlb = False
        ocr = "-"
        id = row[0]
        desc = row[1]
        time = str(row[2])+":"+str(row[3])
        rpt = row[4]
        date = str(row[5])+"-"+str(row[6])+"-"+str(row[7])
        dly = int(row[8]/60)
        if(rpt == "d"):
            rpt = "Every day"
        if(rpt == "w"):
            rpt = "Every week"
        if(rpt == "y"):
            rpt = "Every year"
        if(rpt == "m"):
            rpt = "Every month"
        if(rpt == "c"):
            rpt = "Every "+str(row[11])+" days"
        if(rpt == ''):
            rpt = "-"
        if(dly != 0):
            time = "-"
            date = "-"
            dly = str(dly)+" minutes"
        else:
            dly = "-"
        if(row[10] == 1 and rpt == "-"):
            ocr = "Yes"
        elif(row[10] == 0 and rpt == "-"):
            ocr = "No"
        
        t.add_row([id,desc,time,rpt,date,dly])
    if(navlb):
        print("Data not found, please enter a valid entry id !")
        return 0
    print("Are you sure you want to delete the following?")        
    print(t.draw())
    try:
        cnfrm = input("Type 'DELETE' for confirmation (press ctrl+c to cancel): ")
        if(cnfrm == "DELETE"):
            pass
        else:
            print("|CANCELLED|\n")
            return 0
    except(KeyboardInterrupt):
        print("\n|CANCELLED|\n")
        return 0
    conn.execute("delete from reminders where rmid = "+str(id))
    conn.commit()

    print("Data deleted")
def reset():
    print("Are you sure to delete everything?")
    try:
        cnfrm = input("Type 'RESET MY APP' for confirmation (press ctrl+c to cancel): ")
        if(cnfrm == "RESET MY APP"):
            pass
        else:
            print("|CANCELLED|\n")
            return 0
    except(KeyboardInterrupt):
        print("\n|CANCELLED|\n")
        return 0
    conn.execute("delete from reminders")
    conn.commit()
    print("Reset completed !")
def snd():
    cursor = conn.execute("select * from alarm_data")
    for i in cursor:
        if(i[0] == 'e'):
            setdata = "d"
            print("Sound Disabled")
        else:
            setdata = "e"
            print("Sound Enabled")
        conn.execute("update alarm_data set sound = '"+setdata+"'")
        conn.commit()
print('Type "\\h" for help, "\\a" for about')
while(True):
    try:
        inp = input("cli_reminder_app:~$ ").lower()
        if(inp == "\\h" or inp == "help"):
            print(hlp)
        elif(inp == "\\a"):
            print(abt)
        elif(inp == "clear"):
            os.system(clrscr)
        elif(inp == "ent"):
            entry()
        elif(inp == "show"):
            show_all()
        elif(inp == "exit"):
            print("Bye !!")
            break
        elif(inp[0:3] == "dlt"):
            try:
                id = int(inp[4:len(inp)].strip(" "))
                dlt(id)
            except:
                print("Invalid or missing operand !!")
        elif(inp == "reset"):
            reset()
        elif(inp == "snd"):
            snd()
        elif(inp.strip() == ""):
            continue
        else:
            print("Invalid input")
    except (KeyboardInterrupt):
        print("\nBye !!")
        break
sleep(3)
