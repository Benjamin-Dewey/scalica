# TODO: make this job run on some kind of schedule
# and actually trigger a mapreduce job and write the
# results into pickledb

import mysql.connector
import pickledb

mydb = mysql.connector.connect(
  host="localhost",
  user="appserver",
  passwd="foobarzoot",
  database="scalica"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM auth_user")

users = mycursor.fetchall()

following_dict = {}

for user in users:
  user_id = user[0]
  mycursor.execute("SELECT * FROM micro_following WHERE follower_id = " + str(user_id))
  followings = mycursor.fetchall()
  following_dict[user_id] = [following[2] for following in followings]

file = open("followRelationships.txt", "w+")
for user in following_dict:
    file.write(user + ",")
    for array in following_dict[user]:
        for id in array:
            file.write(str(id)+"-")
        file.write(",")
    file.write("\n")
file.close()
  
# TODO: start a map reduce job and replace the
# right side of the equal sign with the results
suggestions_dict = following_dict

db = pickledb.load('suggestions.db', False)
for key, value in suggestions_dict.iteritems(): db.set(str(key), value)
db.dump()
