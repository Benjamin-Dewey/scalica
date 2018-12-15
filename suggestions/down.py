from multiprocessing import Pool
import mysql.connector
import pickledb
import os

bucket_path = "lswa-scalica/output/"
output_file_name = "df_output.txt-00000-of-00001"

def handle_suggestions(user):
    user_id = int(user[0])

    cnx = mysql.connector.connect(
      host="localhost",
      user="appserver",
      passwd="foobarzoot",
      database="scalica"
    )
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM micro_following WHERE follower_id = " + str(user_id))
    followees = [followee[2] for followee in cursor.fetchall()]
    print('followees', followees)

    cursor.close()
    cnx.close()

    # read from output_file_name to create suggestions for user_id
    # this is a list of the top ten highest ranked suggested
    # users to follow; if there are no suggestions or the user_id
    # is absent from the file just make an empty array
    suggestions = []

    inputStream = open(output_file_name, 'r')
    input = inputStream.read()
    inputStream.close()
    input = input.split("\n") # Split suggs into array

    # Loop thru array, put all [suggUser, strength] for user_id into suggestions
    for sugg in input:
        if sugg:
            user = int(sugg[sugg.find(",")+1:sugg.find(":")])
            suggUser = int(sugg[0:sugg.find(",")])
            strength = int(sugg[sugg.find(":")+2:len(sugg)])
            if user == user_id and suggUser not in followees: suggestions.append([suggUser, strength])

    # Pick top 3 suggestions
    top_suggestions = [sugg[0] for sugg in sorted(suggestions, key=lambda x: x[1], reverse=True)[:3]]

    db = pickledb.load('suggestions.db', False, False)
    db.set(str(user_id), top_suggestions)
    db.dump()

def download():
    try: # delete the old local output file if it exists
        os.remove(output_file_name)
    except:
        pass

    # download the remote output file from the bucket
    command = "gsutil cp gs://" + bucket_path + output_file_name + " " + output_file_name
    os.system(command)

    if (not os.path.isfile(output_file_name)): return # there was no file to download

    cnx = mysql.connector.connect(
      host="localhost",
      user="appserver",
      passwd="foobarzoot",
      database="scalica"
    )
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM auth_user")
    users = cursor.fetchall()

    cursor.close()
    cnx.close()

    # create a process pool and dispatch
    # a call to handle_suggestions for each user
    pool = Pool()
    pool.map(handle_suggestions, users)

    # delete the remote output file from the bucket
    command = "gsutil rm gs://" + bucket_path + output_file_name
    os.system(command)

if __name__ == '__main__':
    download()
