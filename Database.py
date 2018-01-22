#coding=utf-8
# File Name:  Database.py
# Project Name:  Spotify-Requests-with-Twitter
#
# Created by Michael Gamlem III on January 20, 2018
# Copyright © 2018 Michael Gamlem III. All rights reserved.

from sshtunnel import SSHTunnelForwarder
import pymysql
import datetime
import mysql.connector

# this gets the authorization information to connect to the database
# must be called before making connection
def getDatabaseAuthInfo():
    info = open("databaseConnections.txt")
    databaseAuthInfo = [None] * 10
    i = 0
    while i < len(databaseAuthInfo):
        line = info.readline().split()
        databaseAuthInfo[i] = str(line[2])
        i = i + 1
    info.close()
    sql_hostname = databaseAuthInfo[0]
    sql_username = databaseAuthInfo[1]
    sql_password = databaseAuthInfo[2]
    sql_main_database = databaseAuthInfo[3]
    sql_port = databaseAuthInfo[4]
    ssh_host = databaseAuthInfo[5]
    ssh_user = databaseAuthInfo[6]
    ssh_pass = databaseAuthInfo[7]
    ssh_port = databaseAuthInfo[8]
    sql_ip = databaseAuthInfo[9]
    sql_port = int(sql_port)
    ssh_port = int(ssh_port)
    return sql_hostname, sql_username, sql_password, sql_main_database, sql_port, ssh_host, ssh_user, ssh_pass, ssh_port, sql_ip

# makes database connection
# returns cursor and connection to function that calls it
def connectToDatabase():
    sql_hostname, sql_username, sql_password, sql_main_database, sql_port, ssh_host, ssh_user, ssh_pass, ssh_port, sql_ip = getDatabaseAuthInfo()
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_pass,
            remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        conn = pymysql.connect(host=sql_hostname, user=sql_username,
                               passwd=sql_password, db=sql_main_database,
                               port=tunnel.local_bind_port)
        # query = 'SELECT * FROM `Spotify-with-Twitter`.Tweets;'
        cursor = conn.cursor()
        # cursor.execute(query)
        # data = cursor.fetchall()
        # print(data)
        # # data = pd.read_sql_query(query, conn)
        # conn.close()
        return conn, cursor

def insertTweet(id, username, date, text):
    now = datetime.datetime.now()
    connection, cursor = connectToDatabase()

    # create query
    query = "INSERT INTO `Spotify-with-Twitter`.Tweets(`TweetID`, `TwitterUsername`, `TweetDate`, `TweetText`) VALUES("%s", "%s", "%s", "%s");" % /(id, username, date, text)

    try:
        # Execute the SQL command
        cursor.execute(query)
        # Commit your changes in the database
        connection.commit()
    except:
        # Rollback in case there is any error
        connection.rollback()

    # disconnect from server
    connection.close()


# with SSHTunnelForwarder(
#         (ssh_host, ssh_port),
#         ssh_username=ssh_user,
#         #ssh_pkey=mypkey,
#         ssh_password=ssh_pass,
#         remote_bind_address=(sql_hostname, sql_port)) as tunnel:
#     conn = pymysql.connect(host=sql_hostname, user=sql_username,
#             passwd=sql_password, db=sql_main_database,
#             port=tunnel.local_bind_port)
#     query = 'SELECT * FROM `Spotify-with-Twitter`.Tweets;'
#     cursor = conn.cursor()
#     cursor.execute(query)
#     data = cursor.fetchall()
#     print(data)
#     #data = pd.read_sql_query(query, conn)
#     conn.close()