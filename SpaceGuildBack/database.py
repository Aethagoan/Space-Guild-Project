import sqlite3

# make the connection
conn = sqlite3.connect('example.db')
# give it the schema context... sorta
cursor = conn.cursor()


# begin then commit

conn.execute("BEGIN")
# do shit

# commit or rollback.






# close connection
conn.close()