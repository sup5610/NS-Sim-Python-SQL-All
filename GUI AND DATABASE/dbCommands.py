import sqlite3
import random
import os

def getCommands(): 
    fd = open("database_commands.sql", "r")

    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(";")

    cmdDict = {"results": None, "wolf": None, "jaguar": None, "rabbit": None, "deer": None}
    i = 0
    for key in cmdDict:
        cmdDict[key] = sqlCommands[i]
        i += 1

    return cmdDict

def generateData():
    randNums = []
    for i in range(16):
        if i % 4 == 0:
            randNums.append(random.randint(0, 10))
        else:
            randNums.append(round(random.uniform(0, 5), 3))
    
    return randNums

def internalConnect():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "natural_selection.db")

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    return con, cur

def AddResults(username, testData):
    cmdDict = getCommands()

    data = generateData()
    wolfData = data[0:4]
    jaguarData = data[4:8]
    rabbitData = data[8:12]
    deerData = data[12:16]

    con, cur = internalConnect()

    cur.execute(cmdDict["results"].format(username = username))


    query = "SELECT MAX(RUN_ID) FROM results WHERE RUNNER_ID = ((SELECT USER_ID FROM login WHERE USERNAME = '{username}'))"
    cur.execute(query.format(username = username))
    run_id = cur.fetchone()

    cur.execute(cmdDict["wolf"].format(run_id = run_id[0], population = wolfData[0], atk = wolfData[1], hp = wolfData[2], spd = wolfData[3]))
    cur.execute(cmdDict["jaguar"].format(run_id = run_id[0], population = jaguarData[0], atk = jaguarData[1], hp = jaguarData[2], spd = jaguarData[3]))
    cur.execute(cmdDict["rabbit"].format(run_id = run_id[0], population = rabbitData[0], atk = rabbitData[1], hp = rabbitData[2], spd = rabbitData[3]))
    cur.execute(cmdDict["deer"].format(run_id = run_id[0], population = deerData[0], atk = deerData[1], hp = deerData[2], spd = deerData[3]))

    con.commit()
    con.close()