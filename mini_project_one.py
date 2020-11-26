import sys
import login
import post_question
import search_posts

def main():
    db_name = sys.argv[1]
    user = login.login_page(db_name)
    quit = False
    while not quit:
        print('Hello '+user+ ', what are you going to do?')
        option = input('1->Post a question\n2->Search for a post\n3->Logout\n4->Exit\n')
        if option == '1':
            post_question.posts(db_name,user)
        elif option == '2':
            search_posts.search_posts(db_name,user)
        elif option == '3':
            user = login.login_page(db_name)
        elif option == '4':
            print('Goodbye')
            quit = True
            sys.exit()
        else:
            print('Invalid input. Please try again!\n')

if __name__ == '__main__':
    main()