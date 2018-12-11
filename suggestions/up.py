import mysql.connector
import os

def upload():
    cnx = mysql.connector.connect(
      host="localhost",
      user="appserver",
      passwd="foobarzoot",
      database="scalica"
    )
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM auth_user")
    users = cursor.fetchall()
    
    if len(users) == 0: return

    following_dict = {}
    user_id_index = 0
    followee_id_index = 2
    following_id_index = 3

    for user in users:
      user_id = user[user_id_index]

      cursor.execute("SELECT * FROM micro_following WHERE follower_id = " + str(user_id))
      followings = cursor.fetchall()

      cursor.execute("SELECT * FROM micro_reversefollowing WHERE followee_id = " + str(user_id))
      rev_followings = cursor.fetchall()

      following_dict[user_id] = [
        [following[followee_id_index] for following in followings],
        [following[following_id_index] for following in rev_followings]
      ]

    cursor.close()
    cnx.close()

    file_name = "df_input.txt"
    file = open(file_name, "w+")
    for user in following_dict:
        file.write(str(user) + ",")
        for array in following_dict[user]:
            for id in array:
                file.write(str(id)+"-")
            file.write(",")
        file.write("\n")
    file.close()

    # upload file_name to the bucket
    command = "gsutil cp " + file_name + " gs://lswa-scalica/input/" + file_name
    os.system(command)

if __name__ == '__main__':
    upload()
