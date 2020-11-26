import sqlite3
import random
import datetime
from datetime import date

def add_tag(db_name,pid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    tag = input('Please input a tag:')
    c.execute('SELECT * FROM tags WHERE pid = (?) AND tag = (?);',(pid,tag))
    listA = c.fetchall()
    if len(listA) == 0:
        insert_tag = ('''INSERT INTO tags(pid,tag) VALUES(?,?);''')
        c.execute(insert_tag,[(pid),(tag)])
        conn.commit()
        print('Your tag has been saved.')
    else:
        print('This tag already exists!')

def answer_question(db_name,q_pid,uid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    title = input('Please enter an answer title: ')
    text = input('Please enter the body of your answer: ')
    post_date = date.today().strftime('%Y-%m-%d')
    unique_pid = False
    while not unique_pid:
        #generate pid
        pid = 'p' + ("{:0>3d}".format(random.randint(0,999)))
        #check if pid is unique
        c.execute('SELECT * FROM posts WHERE pid = (?);',(pid,))
        listA = c.fetchall()
        if len(listA) == 0:
            unique_pid = True    
    #insert post_date, pid, and uid into posts
    insert_poster = ('''INSERT INTO posts(pid,pdate,title,body,poster) VALUES(?,?,?,?,?);''')
    c.execute(insert_poster,[(pid),(post_date),(title),(text),(uid)])
    conn.commit()
    #insert text,title,date into answers
    insert_answer = ('''INSERT INTO answers(pid,qid) VALUES(?,?);''')
    c.execute(insert_answer,[(pid),(q_pid)])
    conn.commit()
    #insert pid into tags
    insert_tag = ('''INSERT INTO tags(pid) VALUES(?);''')
    c.execute(insert_tag,[(pid)])
    conn.commit()
    print("Your answer has been posted successfuly.")
    
def edit_post(db_name,pid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    exit = False
    while not exit:
        #ask user to give an option
        action = input('Which part do you want to edit?\nPlease enter:\n1->title\n2->body\n3->exit\n')
        if action == '1':
            new_title = input('Please enter new title: ')
            c.execute('UPDATE posts SET title = (?) WHERE pid = (?);', (new_title,pid))
            conn.commit()
            print('The title of this post has now been updated.')
        elif action == '2':
            new_body = input('Please enter new body: ')
            c.execute('UPDATE posts SET body = (?) WHERE pid = (?);', (new_body,pid))
            conn.commit()
            print('The body of this post has now been updated.')
        elif action == '3':
            exit = True

def give_badge(db_name,pid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT poster FROM posts p WHERE p.pid = (?);',(pid,))
    poster = c.fetchall()[0][0]
    bdate = date.today().strftime('%Y-%m-%d')
    c.execute('SELECT uid FROM ubadges ub ,posts p WHERE p.poster = ub.uid AND ub.bdate = (?) AND p.pid =(?);',(bdate,pid))
    listA = c.fetchall()
    if len(listA) == 0:
        bname = input("Please give a badge name: ")
        insert_poster = ('''INSERT INTO ubadges(uid,bdate,bname) VALUES(?,?,?);''')
        c.execute(insert_poster,[(poster),(bdate),(bname)])
        conn.commit()
        print('The badge has been successfully given to the user.')
    else:
        print('This user has already been given a badge today!')

def mark(db_name,pid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT q.theaid FROM questions q, answers a WHERE a.pid = (?) AND a.qid = q.pid;',(pid,))
    listA = c.fetchall()
    #if the question already has an accepted answer
    if listA[0][0] != None:
        change = input("This post already has an accepted answer.\nDo you want to change it?")
        #if user does not want to change it
        if change.upper() == 'N':
            pass
        #if user wants to change the accepted answer
        elif change.upper() == 'Y':
            c.execute('SELECT q.pid FROM questions q, answers a WHERE q.pid = a.qid AND a.pid = (?);',(pid,))
            p_pid = c.fetchall()[0][0]
            c.execute('UPDATE questions SET theaid = (?) WHERE pid =(?);',(pid,p_pid))
            conn.commit()      
            print("Your change has been saved.")
    else:
        c.execute('SELECT q.pid FROM questions q, answers a WHERE q.pid = a.qid AND a.pid = (?);',(pid,))
        p_pid = c.fetchall()[0][0]
        c.execute('UPDATE questions SET theaid = (?) WHERE pid =(?);',(pid,p_pid))
        conn.commit()
        print("Your change has been saved.")

def vote(db_name,pid,uid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT * FROM votes v WHERE v.pid=(?);',(pid,))
    listA = c.fetchall()
    vdate = date.today().strftime('%Y-%m-%d')
    #vno would be the current vno+1
    vno = len(listA)+1
    c.execute('SELECT * FROM votes v WHERE v.pid=(?) AND v.uid = (?);',(pid,uid))
    listB = c.fetchall()
    if len(listB) == 0:
        insert_vote = ('''INSERT INTO votes(pid,vno,vdate,uid) VALUES(?,?,?,?);''')
        c.execute(insert_vote,[(pid),(vno),(vdate),(uid)])
        conn.commit()
        print('Vote saved!')
    else:
        print('You have alredy voted for this post.')