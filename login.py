import sqlite3
import getpass
import sys
import datetime
from datetime import date

def register(db_name):
    success = False
    conn = sqlite3.connect(db_name)
    c = conn.cursor()    
    while not success:
        uid = input('Please enter your user id: ')
        c.execute('SELECT * FROM users u WHERE u.uid = (?);',(uid,))
        listA = c.fetchall()
        if len(listA) != 0:
            print('This user id has already been used. Please try another id.')
        else:
            success = True
    name = input('Please enter your name: ')
    city = input('Please enter your city: ')
    password = getpass.getpass('Please enter your password: ')
    check = getpass.getpass('Please re-enter your password: ')
    while password != check:
        print('Password does not match. Please try again.')
        password = getpass.getpass('Please enter your password: ')
        check = getpass.getpass('Please re-enter your password: ')
    crdate = date.today().strftime('%Y-%m-%d')
    insert_user = ('''INSERT INTO users(uid,name,pwd,city,crdate) VALUES(?,?,?,?,?);''')
    c.execute(insert_user,[(uid),(name),(password),(city),(crdate)])
    conn.commit()
    print('Successfuly registered!')

def login(db_name):
    exist = False
    conn = sqlite3.connect(db_name)
    c = conn.cursor()        
    while not exist:
        uid = input('Please enter your user id: ')
        c.execute('SELECT * FROM users WHERE uid= (?);',(uid,))
        listB = c.fetchall()
        if len(listB) == 0:
            print('User id does not exist. Please try again')
        else:
            password = getpass.getpass('Please enter your password: ')
            c.execute('SELECT * FROM users WHERE uid= (?) AND pwd = (?);',(uid,password))
            listA = c.fetchall()
            if (len(listA) == 0):
                print('Password incorrect. Please try again.')
            else:
                exist = True
    return uid

def login_page(db_name):
    quit = False
    while not quit:
        option = input("Welcome! Please choose from the following options:\n1->login\n2->register\n3->exit\n")
        if option == '1':
            user = login(db_name)
            quit = True
            return user
        elif option == '2':
            register(db_name)
        elif option == '3':
            print('Goodbye')
            quit = True
            sys.exit()
        else:
            print('Invalid input. Please choose from the options provided.')
            