# coding=utf-8

import MySQLdb

db_name = 'ecity0606'
# Connect to a MySQL database on network.
mysql_db = MySQLdb.connect(db=db_name, user='ecitytest', password='ecitytest',
                           host='10.37.149.5', port=3306)

cursor = mysql_db.cursor()
sql = 'SELECT gid, feedbackid, inspectdetailid, filename, createtime, fastdfs FROM pro_propower_inspection_detail_feedback_file AS t1 WHERE (gid = 1335)'
cursor.execute(sql)

print(cursor.fetchone())
