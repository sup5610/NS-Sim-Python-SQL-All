# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 00:27:45 2022

@author: Marco
"""

import tkinter as tk, sys, time, numpy as np, sqlite3, hashlib, secrets, pandas, os
from tkinter import font as tkfont
from tkinter import ttk
# pandas and seaborn next, then PyTorch
# import self made pytorch library

BGONE = "#212529"
BGTWO = "#6C757C"
BGTHREE = "#CCC5B9"
FGONE = "#DEE2E6"
FGTWO = "#EAE0CC"
FGTHREE = "#EAE0CC"





class log_in():
    def __init__(self, master):
        # master.lift()
        master.attributes("-topmost", True)
        master.overrideredirect(True)


        # normal_font = tkfont.Font(family = "Verdana", size = 10)
        # bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
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


        init_window(self, self.root, 150, 75)

        


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
        self.enter_button.config(text = "Log in", command = lambda : self.validate(), relief = tk.GROOVE, bg = BGTWO, fg = FGONE, activebackground = FGONE, activeforeground = BGTWO)
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
    
    def minimise_function(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state("iconic")

    def mapped(self, event):
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state("normal")

    def close_window(self):
        self.root.destroy()
        sys.exit(0)
    
    def enter_enter(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGONE)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGONE)
    def x_enter(self, event):
        self.x_button.config(bg = BGTWO)
    def x_leave(self, event):
        self.x_button.config(bg = BGONE, fg = FGONE)
    def full_enter(self, event):
        self.fullscreen.config(bg = BGTWO)
    def full_leave(self, event):
        self.fullscreen.config(bg = BGONE, fg = FGONE)
    def mini_enter(self, event):
        self.minimise.config(bg = BGTWO)
    def mini_leave(self, event):
        self.minimise.config(bg = BGONE, fg = FGONE)
    

    def window_pos(self, event):
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        print(self.offset_x, self.offset_y)

    def move_window(self, event):
        self.delta_x = self.root.winfo_pointerx() - self.offset_x
        self.delta_y = self.root.winfo_pointery() - self.offset_y
        self.x_pos = self._init_x + self.delta_x
        self.y_pos = self._init_y + self.delta_y
        self.root.geometry("+{x}+{y}".format(x = self.x_pos, y = self.y_pos))
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        self._init_x = self.x_pos
        self._init_y = self.y_pos

        
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
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "natural_selection.db")

        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
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
            self.admin_session = admin(a) # starts admin session
            a.mainloop()
        else:
            self.root.destroy()

            u = tk.Tk()
            self.user_session = user(u) # starts user session
            u.mainloop()

        

    ###########################################################################################################################


###########################################################################################################################


class admin():
    def __init__(self, master):
        master.overrideredirect(True)
        # normal_font = tkfont.Font(family = "Verdana", size = 10)
        # bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
        

        self.root = master
        init_window(self, self.root, 150, 75)
        

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
        new_user(rot)
        rot.mainloop()

    
    def create_edit_users_window(self):
        self.root.destroy()
        rot = tk.Tk()
        edit_users(rot)
        rot.mainloop()

    
    ###########################################################################################################################

    def minimise_function(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state("iconic")

    def mapped(self, event):
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state("normal")

    def close_window(self):
        self.root.destroy()
        sys.exit(0)
    
    
    def enter_enter(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGONE)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGONE)
    def x_enter(self, event):
        self.x_button.config(bg = BGTWO)
    def x_leave(self, event):
        self.x_button.config(bg = BGONE, fg = FGONE)
    def full_enter(self, event):
        self.fullscreen.config(bg = BGTWO)
    def full_leave(self, event):
        self.fullscreen.config(bg = BGONE, fg = FGONE)
    def mini_enter(self, event):
        self.minimise.config(bg = BGTWO)
    def mini_leave(self, event):
        self.minimise.config(bg = BGONE, fg = FGONE)

    def window_pos(self, event):
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        print(self.offset_x, self.offset_y)

    def move_window(self, event):
        self.delta_x = self.root.winfo_pointerx() - self.offset_x
        self.delta_y = self.root.winfo_pointery() - self.offset_y
        self.x_pos = self._init_x + self.delta_x
        self.y_pos = self._init_y + self.delta_y
        self.root.geometry("+{x}+{y}".format(x = self.x_pos, y = self.y_pos))
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        self._init_x = self.x_pos
        self._init_y = self.y_pos


class new_user():
    def __init__(self, master):
        # master.lift()
        master.attributes("-topmost", True)
        master.overrideredirect(True)

        normal_font = tkfont.Font(family = "Verdana", size = 10)
        bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
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
        if (self.feedback_label["text"] != ""):
            self.feedback_label["text"] = ""
    ########################################################################################################################### 
    def validate_username(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "natural_selection.db")

        con = sqlite3.connect(db_path)
        cur = con.cursor()

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
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "natural_selection.db")

        con = sqlite3.connect(db_path)
        cur = con.cursor()

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

    def minimise_function(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state("iconic")

    def mapped(self, event):
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state("normal")

    def close_window(self):
        self.root.destroy()
        sys.exit(0)
    
    def enter_enter(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGTWO)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGONE)
    def x_enter(self, event):
        self.x_button.config(bg = BGTWO)
    def x_leave(self, event):
        self.x_button.config(bg = BGONE, fg = FGONE)
    def full_enter(self, event):
        self.fullscreen.config(bg = BGTWO)
    def full_leave(self, event):
        self.fullscreen.config(bg = BGONE, fg = FGONE)
    def mini_enter(self, event):
        self.minimise.config(bg = BGTWO)
    def mini_leave(self, event):
        self.minimise.config(bg = BGONE, fg = FGONE)

    def window_pos(self, event):
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        print(self.offset_x, self.offset_y)

    def move_window(self, event):
        self.delta_x = self.root.winfo_pointerx() - self.offset_x
        self.delta_y = self.root.winfo_pointery() - self.offset_y
        self.x_pos = self._init_x + self.delta_x
        self.y_pos = self._init_y + self.delta_y
        self.root.geometry("+{x}+{y}".format(x = self.x_pos, y = self.y_pos))
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        self._init_x = self.x_pos
        self._init_y = self.y_pos


class edit_users():
    def __init__(self, master):
        # master.lift()
        master.attributes("-topmost", True)
        master.overrideredirect(True)
        
        master.bind("<KeyPress>", self.filter)


        self.root = master
        # normal_font = tkfont.Font(family = "Verdana", size = 10)
        # bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "natural_selection.db")

        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
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
        self.filter_button.config(text = "Filter", bg = BGONE, fg = FGONE, activebackground = BGTWO, activeforeground = FGTWO, command = lambda : self.filter(event = None))
        self.filter_button.bind("<Enter>", self.filter_enter)
        self.filter_button.bind("<Leave>", self.filter_leave)

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
        self.delete_button.config(text = "Delete User", bg = BGONE, fg = FGONE, activebackground = BGTWO, activeforeground = FGTWO, command = lambda : self.delete_user())
        self.delete_button.bind("<Enter>", self.delete_enter)
        self.delete_button.bind("<Leave>", self.delete_leave)

        self.new_username_label = tk.Label(self.canvas)
        self.new_username_label.grid(row = 1, column = 0)
        self.new_username_label.config(text = "New Username", bg = BGTWO, fg = FGONE)
        self.new_username_entry = tk.Entry(self.canvas)
        self.new_username_entry.grid(row = 1, column = 1)
        self.new_username_entry.config()
        self.change_username_button = tk.Button(self.canvas)
        self.change_username_button.grid(row = 1, column = 2)
        self.change_username_button.config(text = "Change Username", bg = BGONE, fg = FGONE, activebackground = BGTWO, activeforeground = FGTWO, command = lambda : self.change_username())
        self.change_username_button.bind("<Enter>", self.change_username_enter)
        self.change_username_button.bind("<Leave>", self.change_username_leave)


        self.new_password_label = tk.Label(self.canvas)
        self.new_password_label.grid(row = 2, column = 0)
        self.new_password_label.config(text = "New Password", bg = BGTWO, fg = FGONE)
        self.new_password_entry = tk.Entry(self.canvas)
        self.new_password_entry.grid(row = 2, column = 1)
        self.new_password_entry.config()
        self.new_password_button = tk.Button(self.canvas)
        self.new_password_button.grid(row = 2, column = 2)
        self.new_password_button.config(text = "Change Password", bg = BGONE, fg = FGONE, activebackground = BGTWO, activeforeground = FGTWO, command = lambda : self.change_password())
        self.new_password_button.bind("<Enter>", self.change_password_enter)
        self.new_password_button.bind("<Leave>", self.change_password_leave)


    def filter(self, event):
        self.filter_string = ""
        self.filter_string = self.filter_entry.get()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "natural_selection.db")

        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
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
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "natural_selection.db")
            
            self.con = sqlite3.connect(db_path)
            self.cur = self.con.cursor()
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
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "natural_selection.db")

            self.con = sqlite3.connect(db_path)
            self.cur = self.con.cursor()
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
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(BASE_DIR, "natural_selection.db")

                self.con = sqlite3.connect(db_path)
                self.cur = self.con.cursor()
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
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "natural_selection.db")

            self.con = sqlite3.connect(db_path)
            self.cur = self.con.cursor()
            self.cur.execute("UPDATE login SET HASHED_PASS =:hashed, PRE_SALT =:pre_salt, POST_SALT =:post_salt WHERE USERNAME =:sel", {"hashed":self.hashed_password, "pre_salt": self.pre_salt, "post_salt": self.post_salt, "sel": self.selected})

            self.con.commit()
            self.con.close()
            print("password changed")

            self.string_var.set("select user")

            
    def minimise_function(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state("iconic")

    def mapped(self, event):
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state("normal")

    def close_window(self):
        self.root.destroy()
        sys.exit(0)
    
    def enter_enter(self, event):
        self.enter_button.config(bg = BGTWO, fg = FGTWO)
    def enter_leave(self, event):
        self.enter_button.config(bg = BGONE)
    def x_enter(self, event):
        self.x_button.config(bg = BGTWO)
    def x_leave(self, event):
        self.x_button.config(bg = BGONE, fg = FGONE)
    def full_enter(self, event):
        self.fullscreen.config(bg = BGTWO)
    def full_leave(self, event):
        self.fullscreen.config(bg = BGONE, fg = FGONE)
    def mini_enter(self, event):
        self.minimise.config(bg = BGTWO)
    def mini_leave(self, event):
        self.minimise.config(bg = BGONE, fg = FGONE)

    def window_pos(self, event):
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        print(self.offset_x, self.offset_y)

    def move_window(self, event):
        self.delta_x = self.root.winfo_pointerx() - self.offset_x
        self.delta_y = self.root.winfo_pointery() - self.offset_y
        self.x_pos = self._init_x + self.delta_x
        self.y_pos = self._init_y + self.delta_y
        self.root.geometry("+{x}+{y}".format(x = self.x_pos, y = self.y_pos))
        self.offset_x = self.root.winfo_pointerx()
        self.offset_y = self.root.winfo_pointery()
        self._init_x = self.x_pos
        self._init_y = self.y_pos


    def delete_enter(self, event):
        self.delete_button.config(bg = BGTWO)
    def delete_leave(self, event):
        self.delete_button.config(bg = BGONE)
    def filter_enter(self, event):
        self.filter_button.config(bg = BGTWO)
    def filter_leave(self, event):
        self.filter_button.config(bg = BGONE)
    def change_username_enter(self, event):
        self.change_username_button.config(bg = BGTWO)
    def change_username_leave(self, event):
        self.change_username_button.config(bg = BGONE)
    def change_password_enter(self, event):
        self.new_password_button.config(bg = BGTWO)
    def change_password_leave(self, event):
        self.new_password_button.config(bg = BGONE)


###########################################################################################################################


class user():
    def __init__(self, master):
        master.overrideredirect(True)
        

        
        



root = tk.Tk()
normal_font = tkfont.Font(family = "Verdana", size = 10)
bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")

def init_window(self, master, start_x, start_y):

    self._init_x = start_x
    self._init_y = start_y
    master.geometry("+{x}+{y}".format(x = self._init_x, y = self._init_y))

    self.title_bar = tk.Frame(master)
    self.title_bar.pack(expand = 1, side = tk.TOP, fill = tk.X)
    self.title_bar.config(bg = BGONE)
    self.title_bar.bind("<Button-1>", self.window_pos)
    self.title_bar.bind("<B1-Motion>", self.move_window)


    self.canvas = tk.Frame(master)
    self.canvas.pack(expand = 1, side = tk.BOTTOM, fill = tk.BOTH)
    self.canvas.config(bg = BGTWO, width = 600, height = 300)
    self.canvas.bind("<Map>", self.mapped)

    x_button(self)
    fullscreen(self)
    minimise(self)

def x_button(self):
    normal_font = tkfont.Font(family = "Verdana", size = 10)
    bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
    self.x_button = tk.Button(self.title_bar)
    self.x_button.pack(side = tk.RIGHT)
    self.x_button.config(font = bold_font, text = "X", command = lambda : self.close_window(), relief = tk.GROOVE, bg  = BGONE, fg = FGONE, activebackground = BGTHREE, activeforeground = BGONE)
    self.x_button.bind("<Enter>", self.x_enter)
    self.x_button.bind("<Leave>", self.x_leave)

def fullscreen(self):
    normal_font = tkfont.Font(family = "Verdana", size = 10)
    bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
    self.fullscreen = tk.Button(self.title_bar)
    self.fullscreen.pack(side = tk.RIGHT)
    self.fullscreen.config(font = bold_font, text = "☐", relief = tk.GROOVE, bg = BGONE, fg = FGONE, activebackground = BGTHREE, activeforeground = BGONE)
    self.fullscreen.bind("<Enter>", self.full_enter)
    self.fullscreen.bind("<Leave>", self.full_leave)

def minimise(self):
    normal_font = tkfont.Font(family = "Verdana", size = 10)
    bold_font = tkfont.Font(family = "Verdana", size = 9, weight = "bold")
    self.minimise = tk.Button(self.title_bar)
    self.minimise.pack(side = tk.RIGHT)
    self.minimise.config(font = bold_font, text = "—", command = lambda : self.minimise_function(), relief = tk.GROOVE, bg = BGONE, fg = FGONE, activebackground = BGTHREE, activeforeground = BGONE)
    self.minimise.bind("<Enter>", self.mini_enter)
    self.minimise.bind("<Leave>", self.mini_leave)



# log_in(root)
admin(root)



root.mainloop()