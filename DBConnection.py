import pymysql.cursors
import os
from settings import *
DBData = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["database"]

def query(sqlStatement):
    # Database connection
    connection = pymysql.connect(host=DBData["host"],  # your host, usually localhost
                                 user=DBData["user"],  # your username
                                 passwd=DBData["passwd"],  # your password
                                 db=DBData["db"],  # name of the data base
                                 port=DBData["port"],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sqlStatement)
            return (cursor.fetchall())


    finally:
        connection.close()
