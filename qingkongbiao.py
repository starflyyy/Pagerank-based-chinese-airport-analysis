import pymysql
import numpy as np
import csv
List = []
csv_file = csv.reader(open('city_to_from.csv', 'r'))
for stu in csv_file:
    List.append(stu[0])

db = pymysql.connect("localhost", "root", "19980620", "flight")

cursor = db.cursor()
for i in range(len(List)):
    try:
        cursor.execute('select ID_NUM from %s' % List[i])
        result = cursor.fetchall()
        db.commit()
        if (result == ()):
            cursor.execute('drop table %s' % List[i])
            print("drop table %s" % List[i])
    except:
        print("No such table")
    else:
        continue

cursor.close()
db.close()
