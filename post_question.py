import sqlite3
import random
import datetime
from datetime import date

def posts(db_name,uid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    title = input('Please enter a question title: ')
    text = input('Please enter the body of your question: ')
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
    insert_post = ('''INSERT INTO posts(pid,pdate,title,body,poster) VALUES(?,?,?,?,?);''')
    c.execute(insert_post,[(pid),(post_date),(title),(text),(uid)])
    conn.commit()
    #insert pid into questions
    insert_question = ('''INSERT INTO questions(pid) VALUES(?);''')
    c.execute(insert_question,[(pid)])
    conn.commit()
    #insert pid into tags
    insert_tag = ('''INSERT INTO tags(pid) VALUES(?);''')
    c.execute(insert_tag,[(pid)])
    conn.commit()
    print("Your question has been posted successfuly.")