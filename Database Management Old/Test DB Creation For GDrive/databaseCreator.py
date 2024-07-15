import sqlite3

con = sqlite3.connect("natural_selection.db")
cur = con.cursor()

fd = open(r"G:\My Drive\NS Simulator\Version 2 Python Scripts\Database\database_creator.sql", "r") # opens sql file in read mode
sqlFile = fd.read()
fd.close()

sqlCommands = sqlFile.split(";")

for command in sqlCommands:
    cur.execute(command)
con.commit()
con.close()