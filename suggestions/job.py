# TODO: make this job run on some kind of schedule
# and actually trigger a mapreduce job and write the
# results into pickledb

import mysql.connector
import pickledb
import os


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
followee_id = 2
following_id = 3

for user in users:
  user_id = user[0]

  mycursor.execute("SELECT * FROM micro_following WHERE follower_id = " + str(user_id))
  followings = mycursor.fetchall()
  mycursor.execute("SELECT * FROM micro_reversefollowing WHERE followee_id = " + str(user_id))
  rev_followings = mycursor.fetchall()

  following_dict[user_id] = [
    [following[followee_id] for following in followings],
    [following[following_id] for following in rev_followings]
  ]

file = open("followRelationships.txt", "w+")
for user in following_dict:
    file.write(str(user) + ",")
    for array in following_dict[user]:
        for id in array:
            file.write(str(id)+"-")
        file.write(",")
    file.write("\n")
file.close()

os.system('./upload.sh')

# TODO: start a map reduce job and replace the
# right side of the equal sign with the results
suggestions_dict = following_dict

db = pickledb.load('suggestions.db', False)
for key, value in suggestions_dict.iteritems(): db.set(str(key), value)
db.dump()
