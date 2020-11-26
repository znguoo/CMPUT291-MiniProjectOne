import sqlite3
import post_action

def search_posts(db_name,uid):
     conn = sqlite3.connect(db_name)
     c = conn.cursor()
     keys = input("Please provide one or more keywords,split with white space.\n>")
     keys=keys.split()
     posts=[]
     for key in keys:
          #find all posts with keywords
          c.execute('SELECT DISTINCT p.pid,p.pdate,p.title,p.body,p.poster FROM posts p WHERE lower(p.title) like (?) OR lower(p.body) like (?);',('%'+key.lower()+'%','%'+key.lower()+'%'))
          p = c.fetchall()
          posts=list(set(posts).union(set(p)))
          #find all tags with keywords
          c.execute('SELECT DISTINCT p.pid,p.pdate,p.title,p.body,p.poster FROM posts p,tags t WHERE t.pid=p.pid AND lower(t.tag) like (?);',('%'+key.lower()+'%',))
          t = c.fetchall()
          posts=list(set(posts).union(set(t)))
     #stop if no post found
     if len(posts)==0:
          print('NOTHING FOUND.')
          return False
     vote={}
     answers={}
     selection={}
     #count how many times the key apears in posts
     for post in posts:
          for item in post:
               for key in keys:
                    if (key and item)and(key.lower() in item.lower()):
                         if post in selection:
                              selection[post]+=1
                         else:
     
                              selection[post]=1
     #count how many times the key apears in tags                   
     for post in posts:
          c.execute('SELECT t.tag FROM tags t,posts p WHERE p.pid = (?) AND p.pid=t.pid;',(post[0],))
          t=c.fetchall()
          for item in t:
               for key in keys:
                    if (key and item[0])and(key.lower() in item[0].lower()):
                         if post in selection:
                              selection[post]+=1
                         else:
                              selection[post]=1
     #sort posts by keyword appear times
     sortd=sorted(selection.items(),key=lambda x:x[1],reverse=True)
     #make posts at most 5
     posts=[]
     for i in range (100):
          if i<len(sortd):
               posts.append(sortd[i][0])
     num=1
     for p in posts:
          #get vote number
          c.execute('SELECT COUNT(vno) FROM posts p,votes v WHERE p.pid = (?) AND p.pid=v.pid;',(p[0],))
          v=c.fetchall()
          vote[p]=v
          #get answer number
          c.execute('SELECT COUNT(a.pid) FROM posts p,answers a WHERE p.pid = (?) AND p.pid=a.qid;',(p[0],))
          a=c.fetchall()
          answers[p]=a
          print(str(num),p)
          print('  Votes on this post:',vote[p][0][0])
          print('  key:',selection[p])
          num+=1
     #let user choose from the posts found
     valid=[]
     for i in range(len(posts)):
          valid.append(str(i+1))
     msg='Showing '+str(len(posts))+' results. Please choose a post to continue '+str(valid)+':'
     option=input(msg)
     while (option not in valid):
          option=input('Please enter number in'+str(valid)+':')
     if option=='1':
          pid=posts[0][0]
     elif option=='2':
          pid=posts[1][0]
     elif option=='3':
          pid=posts[2][0]
     elif option=='4':
          pid=posts[3][0]    
     elif option=='5':
          pid=posts[4][0]
     c.execute('SELECT uid FROM privileged;')
     p=c.fetchall()
     privileged=False
     for i in p:
          if uid in i:
               privileged=True
     print('1 Answer')
     print('2 Vote')
     if privileged:
          print('3 Mark as the accepted')
          print('4 Give a badge')        
          print('5 Add a tag')
          print('6 Edit')  
     print('0 Exit')
     option=input('Please select the action to do with '+str(pid)+':')
     if privileged==False:
          while (option not in ['1','2','0']):
               option=input("Please select the action from ['1','2','0']:")
     elif privileged==False:
          while (option not in ['1','2','3','4','5','6','0']):
               option=input("Please select the action from ['1','2','3','4','5','6','0']:")     
     if option=='1':
          c.execute('SELECT q.pid FROM posts p,questions q WHERE p.pid = (?) AND p.pid=q.pid;',(pid,))
          q=c.fetchall()
          if q and len(q)!=0:
               post_action.answer_question(db_name,pid,uid)
          else:
               print('This post is not a question!')
     elif option=='2':
          post_action.vote(db_name,pid,uid)
     elif option=='3':
          c.execute('SELECT a.pid FROM posts p,answers a WHERE p.pid = (?) AND p.pid=a.pid;',(pid,))
          a=c.fetchall()
          if len(a)!=0:
               post_action.mark(db_name,pid)
          else:
               print("You cannot make a question as the accepted answer!")
     elif option=='4':
          post_action.give_badge(db_name,pid)
     elif option=='5':
          post_action.add_tag(db_name,pid)
     elif option=='6':
          post_action.edit_post(db_name,pid)
     elif option =='0':
          return True
     
     return True
          
          
          
          
          
          
          
          
          
          
          
