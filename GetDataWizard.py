import re
import pymysql
import os

settings = input("Enter 0 for using Default Settings ( host: localhost , user: root , password: ) \nOR \nEnter Another Key(Except 0) for using Custom Settings\n:")
host = "localhost"
user = "root"
password = ""
if(settings == "0"):
    try:
        db = pymysql.connect(host,user,password)
    except:
        print("Check MySQL Connection")
        os.system("pause")
        os._exit(1)
else:
    host = input("host:")
    user = input("user:")
    password = input("password")
    try:
        db = pymysql.connect(host,user,password)
    except:
        print("Check MySQL Connection")
        os.system("pause")
        os._exit(1)
cursor = db.cursor()
cursor.execute("SHOW DATABASES")
for x in cursor:
    if(str(x[0]) == "fuzzy"):
        print("fuzzy recreated")
        cursor.execute("DROP DATABASE fuzzy")

cursor.execute("CREATE DATABASE fuzzy")
cursor.close()
db.close()
maxValues = {'SO2':1110, 'NO2':2010, 'CO':32010, 'O3':710, 'PM10':530}
db = pymysql.connect("localhost","root","","fuzzy")
cursor = db.cursor()

directory = os.path.join(os.getcwd(),'CSV')
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".csv"):
         tableName = filename[:-4]
         with open(os.path.join(directory, filename)) as fileobj:
             line = fileobj.readline()
             columnValues = ""
             columns = line.split(",")
             columns[len(columns) - 1] = columns[len(columns) - 1].replace("\n", "")
             columnsString = ""
             for i in columns:
                 if (i == "Tarih"):
                     columnsString = columnsString + "Tarih VARCHAR(20) NOT NULL,"
                 elif (i == "Zaman"):
                     columnsString = columnsString + "Zaman VARCHAR(10) NOT NULL,"
                 else:
                     columnsString = columnsString + i + " DOUBLE NULL DEFAULT NULL,"
                 columnValues = columnValues + "%s,"
             sqlCreateTable = "CREATE TABLE " + tableName + "(" + columnsString + " PRIMARY KEY(Tarih, Zaman)) COLLATE=latin5_turkish_ci"
             sqlInsert = "INSERT INTO " + tableName + "(" + line[:-1] + ") VALUES (" + columnValues[:-1] + ")"
             cursor.execute(sqlCreateTable)
             db.commit()
             for line in fileobj:
                 preline = line
                 for m in re.finditer(r"\"-?\d*,\d*\"", line):
                     newstr = m.group()[1:len(m.group()) - 1]
                     newstr = newstr.replace(",", ".")
                     line = line.replace(m.group(), newstr)
                 line = line.replace("\n", "")
                 val = line.split(",")
                 val2 = []
                 for i in val:
                     if i == '':
                         val2.append(None)
                     else:
                         val2.append(i)
                 try:
                     cursor.execute(sqlInsert, val2)
                     db.commit()
                 except:
                     print("line cant insterted: ", line)
                     print("preline: ", preline)

             deleteStr = ""  #DELETE NULL LİNES
             for i in columns[2:]:
                deleteStr = deleteStr + i + " IS NULL AND "
             deleteStr = deleteStr[:-4]
             sqlDelete = "DELETE FROM "+tableName+" WHERE ("+deleteStr+")"
             cursor.execute(sqlDelete)

             for i in columns[2:]: #LİMİT COLUMNS
                 sqlLimit = "UPDATE " + tableName + " SET " + i + " = " + str(maxValues[i]) + " WHERE " + i + " >" + str(maxValues[i]) + ""
                 cursor.execute(sqlLimit)

             for i in columns[2:]: #fill null columns with average
                sqlAVG = "SELECT AVG("+i+") FROM "+tableName+""
                cursor.execute(sqlAVG)
                avarage = cursor.fetchone()
                avarage = ("%.2f" % round(avarage[0],2))
                sqlUpdate = "UPDATE " + tableName + " SET "+i+" = "+avarage+" WHERE "+i+" IS NULL;"
                cursor.execute(sqlUpdate)
             print(filename + " was complete.")
         continue
     else:
         continue




cursor.close()
db.close()
os.system("pause")