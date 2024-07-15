# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 00:27:45 2022

@author: Marco
"""

import tkinter as tk, sys, time, numpy as np, sqlite3, hashlib, secrets, pandas, os, random, seaborn, socket, json, math, uuid
from tkinter import font as tkfont
from tkinter import ttk
from dbCommands import *
# from PopultaionModel import * # where is this file?? u misspelt it u fucking idiot
from PopulationModel import *
socket.setdefaulttimeout(1)


BGONE = "#212529"
BGTWO = "#6C757C"
BGTHREE = "#CCC5B9"
FGONE = "#DEE2E6"
FGTWO = "#EAE0CC"
FGTHREE = "#EAE0CC"

global is_maximised
is_maximised = False

host, port = "127.0.0.1", 64738
global sock
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port))
except:
    print("Connection not open on from Unity")



class log_in():
    def __init__(self, master):
        master.attributes("-topmost", True)
        master.overrideredirect(True)


        self.root = master # self.root variable created to destroy window
        self.details = ["", ""] # username and password inputs
        self.x = [] # all x values of cursor where an event occurs
        self.y = [] # all y values of cursor where an event occurs
        self.username_accepted = False
        self.password_accepted = False
        self.details_accpted = False
        
        self.pre_salt = "" # pre salt for password
        self.post_salt = "" # post salt for password
        self.salted_password = "" # stores salted entered password
        self.hashed_password = "" # stored hashed salted password
        self.stored_data = ("", "")
        
        master.bind("<KeyPress>", self.store)
        master.bind("<Button-1>", self.store)
        master.bind("<Button-2>", self.store)


        init_window(self, master, 150, 75)


        self.pad2 = tk.Label(self.canvas)
        self.pad2.grid(row = 0, column = 0, columnspan = 5)
        self.pad2.config(bg = BGTWO)

        self.pad3 = tk.Label(self.canvas)
        self.pad3.grid(row = 0, column = 0, rowspan = 5)
        self.pad3.config(bg = BGTWO)

        # misc. label"
        self.label1 = tk.Label(self.canvas)
        self.label1.grid(row = 1, column = 1)
        self.label1.config(text = "Log in", font = bold_font, bg = BGTWO, fg = FGONE)       
        
        # username label and entry
        self.username_label = tk.Label(self.canvas)
        self.username_label.grid(row = 2, column = 1)
        self.username_label.config(text = "Username", font = normal_font, bg = BGTWO, fg = FGONE)
        self.username_entry = tk.Entry(self.canvas)
        self.username_entry.grid(row = 2, column = 2)
        self.username_entry.config()
        self.username_entry.focus_set()

        # password label and entry
        self.password_label = tk.Label(self.canvas)
        self.password_label.grid(row = 3, column = 1)
        self.password_label.config(text = "Password", font = normal_font, bg = BGTWO, fg = FGONE)
        self.password_entry = tk.Entry(self.canvas)
        self.password_entry.grid(row = 3, column = 2)
        self.password_entry.config(show = "●")
        self.i = tk.IntVar()
        self.show_password = tk.Checkbutton(self.canvas)
        self.show_password.grid(row = 3, column = 3)
        self.show_password.config(bg = BGTWO, fg = FGONE, activebackground = BGTWO, activeforeground = FGONE, text = "show password", variable = self.i)
        self.show_password.bind("<Button-1>", self.hide_show)

        # button to enter
        self.enter_button = tk.Button(self.canvas)
        self.enter_button.grid(row = 3, column = 4)
        self.enter_button.config(text = "Log in", command = lambda : self.validate(), relief = tk.GROOVE, bg = BGTWO, fg = FGONE, activebackground = BGONE, activeforeground = FGTWO)
        self.enter_button.bind("<Enter>", self.enter_enter)
        self.enter_button.bind("<Leave>", self.enter_leave)
        
        # label to feedback to user
        self.label2 = tk.Label(self.canvas)
        self.label2.grid(row = 4, column = 2)
        self.label2.config(font = bold_font, bg = BGTWO, fg = FGONE)

        self.clock_function(self.canvas)

    ###########################################################################################################################
    def clock_function(self, window):
        # clock
        self.ct = time.strftime("%H:%M:%S")
        self.clock_frame = tk.Frame(window)
        self.clock_frame.grid(row = 0, column = 5)
        self.clock_frame.config(bg = FGONE, bd = 1)
        self.clock_display = tk.Label(self.clock_frame)
        self.clock_display.grid(row = 0, column = 0)
        self.clock_display.config(text = self.ct, width = 6, bg = BGTWO, fg = FGONE)

        self.ct = time.strftime("%H:%M:%S")
        self.clock_display["text"] = self.ct
        window.after(1000, lambda : self.clock_function(window))
    ###########################################################################################################################
    # hide and show password in entry
    def hide_show(self, event):
        if self.i.get() == 0:
            self.password_entry.config(show = "")
        else:
            self.password_entry.config(show = "●")

    # clear the userename and password entries
    def clear_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.details = ["", ""]

    # function stores data
    def store(self, event):
        self.details[0] = self.username_entry.get()
        self.details[1] = self.password_entry.get()
        print(self.details)
        print(event)
        self.x.append(event.x)
        self.y.append(event.y)
        
        if event.keycode == 13: # enter
            self.validate()
        elif event.keycode == 17: # ctrl
            self.xy()
            
    # function prints mean x and y values of cursor
    def xy(self):
        print("Mean X: " + str(np.mean(self.x, dtype = "float64")))
        print("Mean Y: " + str(np.mean(self.y, dtype = "float64")))

    ###########################################################################################################################
    # functions hash entered password
    def saltify(self):
        self.pre_salt = self.stored_data[3]
        self.post_salt = self.stored_data[4]
        self.salted_password = self.pre_salt + self.details[1] + self.post_salt
        
    def hashify(self):
        self.hashed_password = hashlib.sha512(self.salted_password.encode()).hexdigest()
        
    def process_password(self):
        self.saltify()
        self.hashify()
    ###########################################################################################################################
    # functions validate entered username and password
    def download_data(self):
        con, cur = connectDB()
        
        cur.execute("SELECT * FROM login WHERE username=:usn", {"usn":self.details[0]})
        self.stored_data = cur.fetchone()
        
        con.commit()
        con.close()

    ###########################################################################################################################
    def validate(self):
        self.download_data()
        self.validate_username()
        if self.username_accepeted == True:
            self.validate_password()
            if self.password_accepeted == True:
                self.details_accepeted()
            else:
                self.password_rejected()    
        else:
            self.username_rejected()
        
        
        self.username_entry.focus_set()   
        
    def validate_username(self):
        if self.stored_data == None:
            self.username_accepeted = False
            self.password_accepeted = False
        else:
            self.username_accepeted = True           

    def username_rejected(self):
        self.clear_entries()
        self.label2["text"] = "Invalid Details"
        self.username_accepeted = False
        self.password_accepeted = False

    def validate_password(self):
        if self.stored_data == None:
            self.username_accepeted = False
            self.password_accepeted = False
        else:
            self.process_password()
            if self.hashed_password == self.stored_data[2]:
                self.password_accepeted = True
            else:
                self.password_accepeted = False

    def password_rejected(self):
        self.clear_entries()
        self.label2["text"] = "Invalid Details"
        self.username_accepeted = False
        self.password_accepeted = False

    def details_accepeted(self):
        self.label2["text"] = "Access Granted"
        self.details_accepeted = True

        if self.stored_data[5] == 1: # if admin
            self.root.destroy()
            
            a = tk.Tk()
            self.admin_session = admin(a, self.details[0]) # starts admin session
            a.mainloop()
        else:
            self.root.destroy()

            u = tk.Tk()
            self.user_session = user(u, self.details[0]) # self.details[0] is the username, starts user session
            u.mainloop()

    def enter_enter(self, event):
        self.enter_button.config(bg = BGONE, fg = FGONE)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGONE)

class admin():
    def __init__(self, master, user):
        master.attributes("-topmost", True)
        master.overrideredirect(True)

        self.root = master
        init_window(self, master, 150, 75)
        

        self.instruct_label = tk.Label(self.canvas)
        self.instruct_label.grid(column = 0, row = 0)
        self.instruct_label.config(text = "Admin options:", bg = BGTWO, fg = FGONE)

        self.new_user_button = tk.Button(self.canvas)
        self.new_user_button.grid(row = 1, column = 0)
        self.new_user_button.config(text = "Create New User", width = 20, command = lambda : self.create_new_user_window())
    
        self.edit_users_button = tk.Button(self.canvas)
        self.edit_users_button.grid(row = 2, column = 0)
        self.edit_users_button.config(text = "Edit User Details", width = 20, command = lambda : self.create_edit_users_window())


    def create_new_user_window(self):
        self.root.destroy()
        rot = tk.Tk()
        new_user(rot, user)
        rot.mainloop()

    
    def create_edit_users_window(self):
        self.root.destroy()
        rot = tk.Tk()
        edit_users(rot, user)
        rot.mainloop()
    ########################################################################################################################### 
    def enter_enter(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGONE)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGONE)

class new_user():
    def __init__(self, master, user):
        master.attributes("-topmost", True)
        master.overrideredirect(True)

        self.root = master
        self.details = ["", "", ""]
        self.x = []
        self.y = []
        self.options = ["user", "admin"]

        master.bind("<KeyPress>", self.store)
        master.bind("<Button-1>", self.store)
        master.bind("<Button-2>", self.store)


        init_window(self, master, 150, 75)


        self.username_label = tk.Label(self.canvas)
        self.username_label.grid(row = 0, column = 0)
        self.username_label.config(text = "New Username", bg = BGTWO, fg = FGONE)
        self.new_username = tk.Entry(self.canvas)
        self.new_username.grid(row = 0, column = 1)
        self.new_username.config()
        self.new_username.focus_set()

        self.password_label = tk.Label(self.canvas)
        self.password_label.grid(row = 1, column = 0)
        self.password_label.config(text = "New Password", bg = BGTWO, fg = FGONE)
        self.new_password = tk.Entry(self.canvas)
        self.new_password.grid(row = 1, column = 1)
        self.new_password.config(show = "●")

        self.password_conf_label = tk.Label(self.canvas)
        self.password_conf_label.grid(row = 2, column = 0)
        self.password_conf_label.config(text = "Confirm Password", bg = BGTWO, fg = FGONE)
        self.password_conf = tk.Entry(self.canvas)
        self.password_conf.grid(row = 2, column = 1)
        self.password_conf.config(show = "●")

        self.permissions_label = tk.Label(self.canvas)
        self.permissions_label.grid(row = 3, column = 0)
        self.permissions_label.config(text = "Permissions:", bg = BGTWO, fg = FGONE)

        self.string_var = tk.StringVar(self.canvas)
        self.string_var.set("user")
        self.admin_or_not = tk.OptionMenu(self.canvas, self.string_var, *self.options)
        self.admin_or_not.grid(row = 3, column = 1)
        self.admin_or_not.config(bg = BGTWO, fg = FGONE, bd = 0)
        self.admin_or_not["menu"].config(bg = BGTWO, fg = FGTWO)

        self.enter_button = tk.Button(self.canvas)
        self.enter_button.grid(row = 4, column = 0)
        self.enter_button.config(text = "Create", command = self.add_user, bg = BGTWO, fg = FGONE, activebackground = BGONE, activeforeground = FGTWO)

        self.feedback_label = tk.Label(self.canvas)
        self.feedback_label.grid(row = 4, column = 1, columnspan = 3)
        self.feedback_label.config(font = bold_font, width = 30, justify = tk.LEFT, anchor = tk.W, bg = BGTWO, fg = FGONE)

        self.back_button = tk.Button(self.canvas)
        self.back_button.grid(row = 4, column = 3)
        self.back_button.config(text = "Back", bg = BGONE, fg = FGONE, activebackground = BGTWO, activeforeground = BGONE, command = lambda : self.back_to_admin())
        self.back_button.bind("<Enter>", self.back_enter)
        self.back_button.bind("<Leave>", self.back_leave)
        

        self.clock_function(self.canvas)
    ###########################################################################################################################
    def clock_function(self, window):
        # clock
        self.ct = time.strftime("%H:%M:%S")
        self.clock_frame = tk.Frame(window)
        self.clock_frame.grid(row = 0, column = 5)
        self.clock_frame.config(bg = FGONE, bd = 1)
        self.clock_display = tk.Label(self.clock_frame)
        self.clock_display.grid(row = 0, column = 0)
        self.clock_display.config(text = self.ct, width = 6, bg = BGTWO, fg = FGONE)

        self.ct = time.strftime("%H:%M:%S")
        self.clock_display["text"] = self.ct
        window.after(1000, lambda : self.clock_function(window))
        # if (self.feedback_label["text"] != ""): # test for autoclear label. sloppy
        #     self.feedback_label["text"] = ""
    ########################################################################################################################### 
    def validate_username(self):

        con, cur = connectDB()
        cur.execute("SELECT USERNAME FROM login WHERE USERNAME =:usn", {"usn": self.details[0]})
        self.return_user = cur.fetchall()

        con.commit()    
        con.close()

        if len(self.return_user) == 0 and self.details[0] != "":
            self.valid_username = True
        else:
            self.valid_username = False

    def password_confirmed(self):
        if self.details[1] == self.details[2]:
            self.passwords_the_same = True
        else:
            self.passwords_the_same = False

    def encrypt_password(self):
        self.pre_salt = secrets.token_hex(16)
        self.post_salt = secrets.token_hex(16)
        self.new_salted_password = self.pre_salt + self.details[1] + self.post_salt
        self.new_hashed_password = hashlib.sha512(self.new_salted_password.encode()).hexdigest()

        self.commit_details()

    def commit_details(self):
        if self.string_var.get() == "user":
            self.is_admin = 0
        elif self.string_var.get() == "admin":
            self.is_admin = 1
        self.insert_details = (self.details[0], self.new_hashed_password, self.pre_salt, self.post_salt, self.is_admin)
        
        con, cur = connectDB()

        cur.execute("INSERT INTO login (USERNAME, HASHED_PASS, PRE_SALT, POST_SALT, ADMIN) VALUES (?, ?, ?, ?, ?)", self.insert_details)

        con.commit()
        con.close()

        print("committed")
        self.new_username.delete(0, tk.END)
        self.new_password.delete(0, tk.END)
        self.password_conf.delete(0, tk.END)
        self.details = ["", "", ""]

    def add_user(self):
        self.validate_username()
        if self.valid_username == False:
            print("invalid username")
            if self.details[0] == "":
                self.feedback_label["text"] = "Invalid Username"
            else:
                self.feedback_label["text"] = "Username already in use"
            self.new_username.delete(0, tk.END)
            self.new_password.delete(0, tk.END)
            self.password_conf.delete(0, tk.END)
            self.details = ["", "", ""]
        elif self.valid_username == True:
            print("valid username")
            self.password_confirmed()
            if self.passwords_the_same == False:
                print("passwords not matched")
                self.new_password.focus_set()
                self.new_password.delete(0, tk.END)
                self.password_conf.delete(0, tk.END)
                self.details[1] = ""
                self.details[2] = ""
                self.feedback_label["text"] = "Passwords do not match"
            elif self.passwords_the_same == True:
                print("passwords matched")
                self.feedback_label["text"] = ""
                self.encrypt_password()

    def back_to_admin(self):
        self.root.destroy()
        
        a = tk.Tk()
        self.admin_session = admin(a, user) # starts admin session
        a.mainloop()
        
    def store(self, event):
        self.details[0] = self.new_username.get()
        self.details[1] = self.new_password.get()
        self.details[2] = self.password_conf.get()
        print(self.details)
        print(event)
        self.x.append(event.x)
        self.y.append(event.y)

        if event.keycode == 13: # enter
            self.add_user()
        elif event.keycode == 17: # ctrl
            self.xy()

    def xy(self):
        print("Mean X: " + str(np.mean(self.x, dtype = "float64")))
        print("Mean Y: " + str(np.mean(self.y, dtype = "float64")))
    ###########################################################################################################################
    def enter_enter(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGTWO)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGONE)

    def back_enter(self, event):
        self.back_button.config(bg = BGTWO)
    def back_leave(self, event):
        self.back_button.config(bg = BGONE)

class edit_users():
    def __init__(self, master, user):
        master.attributes("-topmost", True)
        master.overrideredirect(True)
        
        master.bind("<KeyPress>", self.filter)

        self.root = master

        self.con, self.cur = connectDB() # fetches all usernames of users
        self.sql = "SELECT USERNAME FROM login WHERE ADMIN = 0"
        self.cur.execute(self.sql)
        self.usernames = self.cur.fetchall()
        self.con.commit()
        self.con.close()

        init_window(self, master, 150, 75)


        self.filter_label = tk.Label(self.canvas)
        self.filter_label.grid(row = 0, column = 0)
        self.filter_label.config(text = "Filter:", bg = BGTWO, fg = FGONE)
        self.filter_entry = tk.Entry(self.canvas)
        self.filter_entry.grid(row = 0, column = 1)
        self.filter_button = tk.Button(self.canvas)
        self.filter_button.grid(row = 0, column = 2)
        self.filter_button.config(text = "Filter", bg = BGTWO, fg = FGONE, activebackground = BGONE, activeforeground = FGTWO, command = lambda : self.filter(event = None))

        self.options = ["select user"]
        for i in range(len(self.usernames)):
            self.options.append(self.usernames[i][0])

        self.string_var = tk.StringVar(self.canvas)
        self.string_var.set("select user")
        self.user_select = tk.OptionMenu(self.canvas, self.string_var, *self.options)
        self.user_select.grid(row = 0, column = 0)
        self.user_select.config(width = 15, bg = BGTWO, fg = FGONE, bd = 0)
        self.user_select["menu"].config(bg = BGTWO, fg = FGTWO)

        self.delete_button = tk.Button(self.canvas)
        self.delete_button.grid(row = 4, column = 0)
        self.delete_button.config(text = "Delete User", bg = BGTWO, fg = FGONE, activebackground = BGONE, activeforeground = FGTWO, command = lambda : self.delete_user())

        self.new_username_label = tk.Label(self.canvas)
        self.new_username_label.grid(row = 1, column = 0)
        self.new_username_label.config(text = "New Username", bg = BGTWO, fg = FGONE)
        self.new_username_entry = tk.Entry(self.canvas)
        self.new_username_entry.grid(row = 1, column = 1)
        self.new_username_entry.config()
        self.change_username_button = tk.Button(self.canvas)
        self.change_username_button.grid(row = 1, column = 2)
        self.change_username_button.config(text = "Change Username", bg = BGTWO, fg = FGONE, activebackground = BGONE, activeforeground = FGTWO, command = lambda : self.change_username())

        self.new_password_label = tk.Label(self.canvas)
        self.new_password_label.grid(row = 2, column = 0)
        self.new_password_label.config(text = "New Password", bg = BGTWO, fg = FGONE)
        self.new_password_entry = tk.Entry(self.canvas)
        self.new_password_entry.grid(row = 2, column = 1)
        self.new_password_entry.config()
        self.new_password_button = tk.Button(self.canvas)
        self.new_password_button.grid(row = 2, column = 2)
        self.new_password_button.config(text = "Change Password", bg = BGTWO, fg = FGONE, activebackground = BGONE, activeforeground = FGTWO, command = lambda : self.change_password())

        self.back_button = tk.Button(self.canvas)
        self.back_button.grid(row = 4, column = 2)
        self.back_button.config(text = "Back", bg = BGONE, fg = FGONE, activebackground = BGTWO, activeforeground = BGONE, command = lambda : self.back_to_admin())
        self.back_button.bind("<Enter>", self.back_enter)
        self.back_button.bind("<Leave>", self.back_leave)

        self.clock_function(self.canvas)
    ###########################################################################################################################
    def clock_function(self, window):
        # clock
        self.ct = time.strftime("%H:%M:%S")
        self.clock_frame = tk.Frame(window)
        self.clock_frame.grid(row = 0, column = 5)
        self.clock_frame.config(bg = FGONE, bd = 1)
        self.clock_display = tk.Label(self.clock_frame)
        self.clock_display.grid(row = 0, column = 0)
        self.clock_display.config(text = self.ct, width = 6, bg = BGTWO, fg = FGONE)

        self.ct = time.strftime("%H:%M:%S")
        self.clock_display["text"] = self.ct
        window.after(1000, lambda : self.clock_function(window))
    ###########################################################################################################################
    def filter(self, event):
        self.filter_string = ""
        self.filter_string = self.filter_entry.get()

        self.con, self.cur = connectDB()
        self.cur.execute("SELECT USERNAME FROM login WHERE USERNAME LIKE :filter", {"filter": "%" + self.filter_string + "%"})
        self.filtered_usernames = self.cur.fetchall()
        self.con.commit()
        self.con.close()

        if event == None or event.keycode == 13:
            self.options = ["select user"]
            self.user_select["menu"].delete(0, tk.END)
            self.user_select["menu"].add_command(label = "select user", command = tk._setit(self.string_var, self.options[0]))
            self.string_var.set("select user")

            for choice in self.filtered_usernames:
                self.options.append(choice[0])
                self.user_select["menu"].add_command(label = choice, command = tk._setit(self.string_var, choice[0]))

    def delete_user(self):
        self.selected = self.string_var.get()

        if self.selected == "select user":
            print("pass")
        else:
            self.con, self.cur = connectDB()
            self.cur.execute("DELETE FROM login WHERE USERNAME =:sel", {"sel": self.selected})
            self.con.commit()
            self.con.close()
            print("user deleted")

            self.string_var.set("select user")
            self.filter_entry.delete(0, tk.END)
            self.new_username_entry.delete(0, tk.END)
            self.new_password_entry.delete(0, tk.END)

            self.filter(event = None)

    def change_username(self):
        self.selected = self.string_var.get()
        self.new_username = self.new_username_entry.get()
        self.valid = False

        if self.new_username == "":
            self.valid = False
            print("username can not be empty")
        else:
            self.con, self.cur = connectDB()
            self.cur.execute("SELECT USERNAME FROM login WHERE USERNAME =:usn", {"usn": self.new_username})
            self.return_username = self.cur.fetchall()
            self.con.commit()
            self.con.close()

            if len(self.return_username) == 0:
                self.valid = True
                print("valid")
            else:
                self.valid = False
                print("username already exists")

        if self.selected == "select user":
            print("pass")
        else:
            if self.valid == True:

                self.con, self.cur = connectDB()
                self.cur.execute("UPDATE login SET USERNAME =:new_usn WHERE USERNAME =:sel", {"new_usn": self.new_username, "sel": self.selected})
                self.con.commit()
                self.con.close()
                print("username changed")

                self.string_var.set("select user")
                self.filter_entry.delete(0, tk.END)
                self.new_username_entry.delete(0, tk.END)
                self.new_password_entry.delete(0, tk.END)
                self.filter(event = None)

    def change_password(self):
        self.selected = self.string_var.get()
        self.new_password = self.new_password_entry.get()

        self.pre_salt = secrets.token_hex(16)
        self.post_salt = secrets.token_hex(16)
        self.salted_password = self.pre_salt + self.new_password + self.post_salt
        self.hashed_password = hashlib.sha512(self.salted_password.encode()).hexdigest()

        if self.selected == "select user":
            print("pass")
        else:
            self.con, self.cur = connectDB()
            self.cur.execute("UPDATE login SET HASHED_PASS =:hashed, PRE_SALT =:pre_salt, POST_SALT =:post_salt WHERE USERNAME =:sel", {"hashed":self.hashed_password, "pre_salt": self.pre_salt, "post_salt": self.post_salt, "sel": self.selected})

            self.con.commit()
            self.con.close()
            print("password changed")

            self.string_var.set("select user")

    def back_to_admin(self):
        self.root.destroy()
        
        a = tk.Tk()
        self.admin_session = admin(a, user) # starts admin session
        a.mainloop()
   
    def enter_enter(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGTWO)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGONE)

    def back_enter(self, event):
        self.back_button.config(bg = BGTWO)
    def back_leave(self, event):
        self.back_button.config(bg = BGONE)

class user():
    def __init__(self, master, user):
        master.attributes("-topmost", True)
        master.overrideredirect(True)
        init_window(self, master, 150, 75)

        self.root = master

        

        

class submit():
    def __init__(self, master, user):
        master.attributes("-topmost", True)
        master.overrideredirect(True)
        init_window(self, master, 150, 75)

        self.root = master

        # self.label = tk.Label()
        # self.label.config(width = 20, height = 20)
        # self.label.pack()

        self.data = generateData()
        self.button = tk.Button(self.canvas)
        self.button.config(text = "Sumbit", command = lambda : AddResults(user, self.data))
        self.button.pack()


    
        
        
class simulation():
    def __init__(self, master, user):
        master.attributes("-topmost", True)
        master.overrideredirect(True)
        init_window(self, master, 150, 75)

        self.root = master


        self.e1 = tk.Entry(self.canvas)
        self.e1.pack()
        self.b1 = tk.Button(self.canvas)
        self.b1.config(text = "Send data", command = lambda : self.SendInfo(self.e1.get()))
        self.b1.pack()


        self.wolvesLabel = tk.Label(self.canvas, text = "{Spawn wolves}: 0", bg = BGTWO)
        self.wolvesLabel.pack()
        self.deerLabel = tk.Label(self.canvas, text = "{Spawn deer}: 0", bg = BGTWO)
        self.deerLabel.pack()
        self.rabbitsLabel = tk.Label(self.canvas, text = "{Spawn rabbits}: 0", bg = BGTWO)
        self.rabbitsLabel.pack()
        self.jaguarsLabel = tk.Label(self.canvas, text = "{Spawn jaguars}: 0", bg = BGTWO)
        self.jaguarsLabel.pack()

        self.wolvesScale = ttk.Scale(self.canvas, name = "wolvesScale", from_ = 0, to = 10, orient = "horizontal", command = self.WolvesEvent)
        self.wolvesScale.pack()
        self.deerScale = ttk.Scale(self.canvas, name = "deerScale", from_ = 0, to = 10, orient = "horizontal", command = self.DeerEvent)
        self.deerScale.pack()
        self.rabbitsScale = ttk.Scale(self.canvas, name = "rabbitsScale", from_ = 0, to = 10, orient = "horizontal", command = self.RabbitsEvent)
        self.rabbitsScale.pack()
        self.jaguarsScale = ttk.Scale(self.canvas, name = "jaguarsScale", from_ = 0, to = 10, orient = "horizontal", command = self.JaguarsEvent)
        self.jaguarsScale.pack()

        self.spawnButton = tk.Button(self.canvas)
        self.spawnButton.config(text = "spawn from slider", command = lambda : self.Spawn())
        self.spawnButton.pack()

    def WolvesEvent(self, value):
        rounded = round(float(value))
        self.wolvesLabel["text"] = "Spawn wolves:", rounded
    def DeerEvent(self, value):
        rounded = round(float(value))
        self.deerLabel["text"] = "Spawn deer:", rounded
    def RabbitsEvent(self, value):
        rounded = round(float(value))
        self.rabbitsLabel["text"] = "Spawn rabbits:", rounded
    def JaguarsEvent(self, value):
        rounded = round(float(value))
        self.jaguarsLabel["text"] = "Spawn jagurs:", rounded

        

    def SendInfo(self, data):
        sent = False
        attempts = 0
        if data == "" or data == None:
            print("Invalid")
        else:
            while (not sent and attempts < 10):
                try:
                    print("sending")
                    sock.sendall(data.encode("UTF-8"))
                    received = sock.recv(1024).decode("UTF-8")
                except:
                    received = False
                    attempts += 1
                    print("socket currently closed")
                    
                time.sleep(0.2)
                if (received == "success"):
                    sent = True
                    print("success")


    def Spawn(self):
        spawnNumbers = {
        "wolf": round(self.wolvesScale.get()),
        "deer": round(self.deerScale.get()),
        "rabbit": round(self.rabbitsScale.get()),
        "jaguar": round(self.jaguarsScale.get())
        }
        
        for i in spawnNumbers.keys():
            for j in range(spawnNumbers[i]):
                self.SendInfo("inst"+i)
                # print("inst"+i)
                # self.SendInfo("inst"+str(spawnNumbers[i]))



        # for i in spawnNumbers.keys():
        #     print(i)
        #     print(spawnNumbers[i])






root = tk.Tk()
normal_font = tkfont.Font(family = "Verdana", size = 10)
bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")

def connectDB():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "natural_selection.db")

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    return con, cur

def init_window(self, master, start_x, start_y):
    def mapped(event):
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state("normal")

    def window_pos(event):
        # offset_x = self.root.winfo_pointerx()
        # offset_y = self.root.winfo_pointery()
        # print(offset_x, offset_y)
        self._offsetx = self.root.winfo_pointerx() - self.root.winfo_rootx()
        self._offsety = self.root.winfo_pointery() - self.root.winfo_rooty()

    def move_window(event):
        # offset_x = self.root.winfo_pointerx()
        # offset_y = self.root.winfo_pointery()
        # delta_x = self.root.winfo_pointerx() - offset_x
        # delta_y = self.root.winfo_pointery() - offset_y

        # x_pos = self._init_x + delta_x
        # y_pos = self._init_y + delta_y
        # self.root.geometry("+{x}+{y}".format(x = x_pos, y = y_pos))
        # self._init_x = x_pos
        # self._init_y = y_pos
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f"+{x}+{y}")

    def resize(event):
        self.root.geometry("{width}x{height}".format(width = event.width, height = event.height))


    _init_x = start_x
    _init_y = start_y
    master.geometry("+{x}+{y}".format(x = _init_x, y = _init_y))

    self.title_bar = tk.Frame(master)
    self.title_bar.pack(expand = 1, side = tk.TOP, fill = tk.X)
    self.title_bar.config(bg = BGONE)
    self.title_bar.bind("<Button-1>", window_pos)
    self.title_bar.bind("<B1-Motion>", move_window)


    self.canvas = tk.Frame(master)
    self.canvas.pack(expand = 1, side = tk.BOTTOM, fill = tk.BOTH)
    self.canvas.config(bg = BGTWO, width = 600, height = 300)
    self.canvas.bind("<Map>", mapped)


    x_button(self)
    fullscreen(self)
    minimise(self)

def x_button(self):
    def close_window(self):
        self.root.destroy()
        sys.exit(0)

    def x_enter(event):
        self.x_button.config(bg = BGTWO)
    def x_leave(event):
        self.x_button.config(bg = BGONE, fg = FGONE)

    normal_font = tkfont.Font(family = "Verdana", size = 10)
    bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
    self.x_button = tk.Button(self.title_bar)
    self.x_button.pack(side = tk.RIGHT)
    self.x_button.config(font = bold_font, text = "X", command = lambda : close_window(self), relief = tk.GROOVE, bg  = BGONE, fg = FGONE, activebackground = BGTHREE, activeforeground = BGONE)
    self.x_button.bind("<Enter>", x_enter)
    self.x_button.bind("<Leave>", x_leave)

def fullscreen(self):
    def set_fullscreen(self):
        global is_maximised
        if is_maximised == False:
            self.root.state("zoomed")
            is_maximised = True
        else:
            self.root.state("normal")
            is_maximised = False

    def full_enter(event):
        self.fullscreen.config(bg = BGTWO)
    def full_leave(event):
        self.fullscreen.config(bg = BGONE, fg = FGONE)

    normal_font = tkfont.Font(family = "Verdana", size = 10)
    bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
    self.fullscreen = tk.Button(self.title_bar)
    self.fullscreen.pack(side = tk.RIGHT)
    self.fullscreen.config(font = bold_font, text = "☐", command = lambda : set_fullscreen(self), relief = tk.GROOVE, bg = BGONE, fg = FGONE, activebackground = BGTHREE, activeforeground = BGONE)
    self.fullscreen.bind("<Enter>", full_enter)
    self.fullscreen.bind("<Leave>", full_leave)

def minimise(self):
    def minimise_function(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state("iconic")

    def mini_enter(event):
        self.minimise.config(bg = BGTWO)
    def mini_leave(event):
        self.minimise.config(bg = BGONE, fg = FGONE)

    normal_font = tkfont.Font(family = "Verdana", size = 10)
    bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
    self.minimise = tk.Button(self.title_bar)
    self.minimise.pack(side = tk.RIGHT)
    self.minimise.config(font = bold_font, text = "—", command = lambda : minimise_function(self), relief = tk.GROOVE, bg = BGONE, fg = FGONE, activebackground = BGTHREE, activeforeground = BGONE)
    self.minimise.bind("<Enter>", mini_enter)
    self.minimise.bind("<Leave>", mini_leave)

def connectSOCK():
    pass




log_in(root)
# admin(root)
# user(root, "user1")
# simulation(root, "user1")


root.mainloop()