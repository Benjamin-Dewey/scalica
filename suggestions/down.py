from multiprocessing import Pool
import mysql.connector
import pickledb
import os

file_name = "suggestions_data.txt"

def handle_suggestions(user):
    user_id = user[0]

    # read from file_name to create suggestions for user_id
    # this is a list of the top ten highest ranked suggested
    # users to follow; if there are no suggestions or the user_id
    # is absent from the file just make an empty array
    suggestions = [] # TODO

    db = pickledb.load('suggestions.db', False, False)
    db.set(str(user_id), suggestions)
    db.dump()

def download():
    # download the output file from the bucket
    command = "gsutil cp gs://scalica-bucket/output/file.txt " + file_name
    os.system(command)

    if (not os.path.isfile(file_name)): return # there was no file to download

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
    # a call to write_suggestions for each user
    pool = Pool()
    pool.map(handle_suggestions, users)

if __name__ == '__main__':
    download()
