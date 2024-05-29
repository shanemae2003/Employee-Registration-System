import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import *
import time

# Global variable to store the currently logged-in user
logged_in_user = None

# Database
conn = sqlite3.connect('payroll.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Users (
             ID INTEGER PRIMARY KEY AUTOINCREMENT,
             Username TEXT,
             Password TEXT,
             LoginTime TEXT,
             LogoutTime TEXT
             )''')

# Function to handle login
def login():
    global logged_in_user
    username = entryUsername.get()
    password = entryPassword.get()

    # Dictionary of usernames and passwords
    credentials = {
        "shane": "shane",
        "admin": "admin",
        "romeo": "romeo",
        # Add more username-password pairs as needed
    }

    # Check if the username and password are correct
    if username in credentials and credentials[username] == password:
        logged_in_user = username
        record_login(username, password)  # Record login time and password in the database
        messagebox.showinfo("Success", "Login successful!")
        root.deiconify()
        loginWindow.destroy()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to record login time in the database
def record_login(username, password):
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    login_time = time.strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO Users (Username, Password, LoginTime) VALUES (?, ?, ?)", (username, password, login_time))
    conn.commit()
    conn.close()

# Function to record logout time in the database
def record_logout(username):
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    logout_time = time.strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE Users SET LogoutTime = ? WHERE Username = ? " , (logout_time, username))
    conn.commit()

# Function to handle logout
def logout():
    record_logout(logged_in_user)  # Record logout time
    messagebox.showinfo("Logout", "Logged out successfully!")
    root.withdraw()
    try:
        entryUsername.delete(0, END)
    except tk.TclError:
        pass


# GUI setup
root = Tk()

# Login window
loginWindow = Toplevel(root)
loginWindow.title('Login')
loginWindow.geometry('300x200')

Label(loginWindow, text='Username').pack()
entryUsername = Entry(loginWindow)
entryUsername.pack()

Label(loginWindow, text='Password').pack()
entryPassword = Entry(loginWindow, show='*')
entryPassword.pack()

Button(loginWindow, text='Login', command=login).pack()

root.withdraw()
root.mainloop()

def create_database():
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS registration
                     (id INTEGER PRIMARY KEY,
                      empname TEXT,
                      posrank TEXT,
                      mobile TEXT,
                      salary REAL,
                      email TEXT,
                      address TEXT)''')

        conn.commit()
        print("Database created successfully.")
    except sqlite3.Error as e:
        print("Error creating database:", e)
    finally:
        conn.close()

if _name_ == "_main_":
    create_database()

def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    e1.insert(0, select['id'])
    e2.insert(0, select['empname'])
    e3.insert(0, select['posrank'])
    e4.insert(0, select['mobile'])
    e5.insert(0, select['salary'])
    e6.insert(0, select['email'])
    e7.insert(0, select['address'])

def Add():
    id = e1.get()
    empname = e2.get()
    posrank = e3.get()
    mobile = e4.get()
    salary = e5.get()
    email = e6.get()
    address = e7.get()

    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO registration (empname, posrank, mobile, salary, email, address) VALUES (?, ?, ?, ?, ?, ?)", (empname, posrank, mobile, salary, email, address))
        conn.commit()
        messagebox.showinfo("Information", "Employee inserted successfully...")
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)

        e2.focus_set()
        show()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def update():
    id = e1.get()
    empname = e2.get()
    posrank = e3.get()
    mobile = e4.get()
    salary = e5.get()
    email = e6.get()
    address = e7.get()

    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()

    try:
        c.execute("UPDATE registration SET empname=?, posrank=?, mobile=?, salary=?, email=?, address=? WHERE id=?", (empname, posrank, mobile, salary, email, address, id))
        conn.commit()
        messagebox.showinfo("Information", "Record updated successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        e1.focus_set()
        show()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def delete():
    id = e1.get()
    empname = e2.get()
    posrank = e3.get()
    mobile = e4.get()
    salary = e5.get()
    email = e6.get()
    address = e7.get()

    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()

    try:
        c.execute("DELETE FROM registration WHERE id=?", (id,))
        conn.commit()
        messagebox.showinfo("Information", "Record deleted successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        e1.focus_set()
        show()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def show():
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()

    try:
        c.execute("SELECT id, empname, posrank, mobile, salary, email, address FROM registration")
        records = c.fetchall()

        # Clear treeview
        for record in listBox.get_children():
            listBox.delete(record)

        for i, (id, empname, posrank, mobile, salary, email, address) in enumerate(records, start=1):
            listBox.insert("", "end", values=(id, empname, posrank, mobile, salary, email, address))
    except Exception as e:
        print(e)
    finally:
        conn.close()

root = Tk()
root.geometry("1200x500")

tk.Label(root, text="Employee Management System", fg="blue", font=(None, 55)).place(x=300, y=70)

tk.Label(root, text="Employee ID").place(x=10, y=10)
Label(root, text="Employee Name").place(x=10, y=40)
Label(root, text="Position Rank").place(x=10, y=70)
Label(root, text="Mobile").place(x=10, y=100)
Label(root, text="Salary").place(x=10, y=130)
Label(root, text="Email").place(x=10, y=160)
Label(root, text="Address").place(x=10, y=190)

e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)

e3 = Entry(root)
e3.place(x=140, y=70)

e4 = Entry(root)
e4.place(x=140, y=100)

e5 = Entry(root)
e5.place(x=140, y=130)

e6 = Entry(root)
e6.place(x=140, y=160)

e7 = Entry(root)
e7.place(x=140, y=190)

Button(root, text="Add", command=Add, height=3, width=13).place(x=70, y=230)
Button(root, text="Update", command=update, height=3, width=13).place(x=190, y=230)
Button(root, text="Delete", command=delete, height=3, width=13).place(x=300, y=230)
Button(root, text="Logout", command=logout, height=3, width=13).place(x=410, y=230)

cols = ('ID', 'Employee Name', 'Position Rank',  'Mobile', 'Salary', 'Email', 'Address')
listBox = ttk.Treeview(root, columns=cols, show='headings')

for col in cols:
    listBox.heading(col, text=col)
listBox.grid(row=1, column=0, columnspan=2)
listBox.place(x=10, y=300)

show()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()
