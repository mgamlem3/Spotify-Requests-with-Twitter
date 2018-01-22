#coding=utf-8
# File Name:  Database.py
# Project Name:  Spotify-Requests-with-Twitter
#
# Created by Michael Gamlem III on January 20, 2018
# Copyright © 2018 Michael Gamlem III. All rights reserved.

from sshtunnel import SSHTunnelForwarder
import pymysql

sql_hostname = '127.0.0.1'
sql_username = 'michael'
sql_password = 'NewPassword#1'
sql_main_database = 'Spotify_Requests_with_Twitter'
sql_port = 3306
ssh_host = '10.211.55.7'
ssh_user = 'michael'
ssh_pass = 'spaceman'
ssh_port = 22
sql_ip = '1.1.1.1.1'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        #ssh_pkey=mypkey,
        ssh_password=ssh_pass,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = pymysql.connect(host=sql_hostname, user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)
    query = 'SELECT * FROM `Spotify-with-Twitter`.Tweets;'
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)
    #data = pd.read_sql_query(query, conn)
    conn.close()