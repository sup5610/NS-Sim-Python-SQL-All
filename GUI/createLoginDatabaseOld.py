# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 16:49:48 2022

@author: Marco
"""

import sqlite3


con = sqlite3.connect("natural_selection.db")
cur = con.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS login
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME VARCHAR(255) NOT NULL,
    HASHED_PASS VARCHAR(1024) NOT NULL,
    PRE_SALT VARCHAR(255) NOT NULL,
    POST_SALT VARCHAR(255) NOT NULL,
    ADMIN INT NOT NULL
    )""")




con.commit()
con.close()
print("database created")