import random
import pymysql
db=pymysql.connect(host="localhost",user="root",password="server123")
mycur=db.cursor()
def create():
    print("")
    try:
        mycur.execute("create database movie_catalog")
        print("Database is created")
    except:
        print("Database already exists")
    mycur.execute("use movie_catalog")
    try:
        mycur.execute("create table movies(movie_id int primary key,movie_name varchar(50),movie_lang varchar(20),movie_genre varchar(20),movie_year int,imdb_rating float(2,1),imdb_link varchar(50))")
        print("The table 'movies' has been created, now we can add records")
    except:
        print("Table already exists, enter records")
        print("")
        print("Current Records:")
        display()

def drop():
    print("")
    mycur.execute("use movie_catalog")
    mycur.execute("drop database movie_catalog")
    print("The database has been dropped")
    
def add():
    mycur.execute("use movie_catalog")
    print("")
    movie_id=int(input("Enter the movie id:"))
    movie_name=input("Enter the name of the movie:")
    movie_lang=input("Enter the language of the movie:")
    movie_genre=input("Enter the genre of the movie:")
    movie_year=int(input("Enter the release year of the movie:"))
    imdb_rating=float(input("Enter the imdb rating of the movie:"))
    imdb_link=input("Enter the imdb link to the movie:")
    sql="insert into movies values({},'{}','{}','{}',{},{},'{}')".format(movie_id,movie_name.lower(),movie_lang.lower(),movie_genre.lower(),movie_year,imdb_rating,imdb_link.lower())
    mycur.execute(sql)
    db.commit()      

def edit():
    mycur.execute("use movie_catalog")
    print("")
    movie_id=int(input("Enter the movie id:"))
    sql="select count(*) from movies where movie_id={}".format(movie_id,)
    mycur.execute(sql)
    r=mycur.fetchone()
    if r==None:
        print("Movie does not exist in the database")
    else:
        print("What do you want to edit?")
        print("1. Movie Name(1)")
        print("2. Movie Language(2)")
        print("3. Movie Genre(3)")
        print("4. Movie Year(4)")
        print("5. IMDb Rating(5)")
        print("6. IMDb Link(6)")
        x=int(input(""))
        if x in [1,2,3,4,5,6]:
            if x==1:
                movie_name=input("Enter the new movie name:")
                sql="update movies set movie_name='{}' where movie_id={}".format(movie_name.lower(),movie_id)
            elif x==2:
                movie_lang=input("Enter the new movie language:")
                sql="update movies set movie_lang='{}' where movie_id={}".format(movie_lang.lower(),movie_id)
            elif x==3:
                movie_genre=input("Enter the new movie genre:")
                sql="update movies set movie_genre='{}' where movie_id={}".format(movie_genre.lower(),movie_id)
            elif x==4:
                movie_year=input("Enter the new movie release year:")
                sql="update movies set movie_year={} where movie_id={}".format(movie_year,movie_id)
            elif x==5:
                imdb_rating=input("Enter the new movie IMDb rating:")
                sql="update movies set imdb_rating={} where movie_id={}".format(imdb_rating,movie_id)
            elif x==6:
                imdb_link=input("Enter the new movie imdb link:")
                sql="update movies set imdb_link='{}' where movie_id={}".format(imdb_link.lower(),movie_id)
            mycur.execute(sql)
            db.commit()
        else:
            print("Invalid Input")

def display():
    mycur.execute("use movie_catalog")
    sql="select * from movies"
    mycur.execute(sql)
    print("")
    print("All movie records:")
    for i in mycur.fetchall():
        print(i)

def browse():
    mycur.execute("use movie_catalog")
    print("Languages: Hindi or English")
    movie_lang=input("Choose preferred language of the movie:")
    print("Genres: Drama, Crime, Thriller, Comedy, Horror, Action, Fiction, Biopic, Sports")
    movie_genre=input("Choose preferred genre of the movie:")
    sql="select * from movies where movie_lang='{}' and movie_genre='{}' order by imdb_rating".format(movie_lang.lower(),movie_genre.lower())
    try:
        mycur.execute(sql)
        print("")
        for i in mycur.fetchall():
            print(i)
    except:
        print("No data found")

def find():
    mycur.execute("use movie_catalog")
    movie_name=input("Enter the movie name:")
    sql="select * from movies where movie_name='{}'".format(movie_name.lower(),)
    mycur.execute(sql)
    print("")
    for i in mycur.fetchall():
        print(i)

def randomize():
    imdb_rating=eval(input("Select the lowest IMDb rating for the movie or enter '0' to keep no limit:"))
    mycur.execute("use movie_catalog")
    mycur.execute("select * from movies where imdb_rating>={}".format(imdb_rating,))
    first_record=mycur.fetchone()
    first_id=first_record[0]
    last_id=mycur.rowcount
    movie_id=random.randint(first_id,last_id)
    sql="select * from movies where movie_id={}".format(movie_id,)
    mycur.execute(sql)
    random_movie=mycur.fetchone()
    print("")
    print("Movie Id:",random_movie[0])
    print("Movie Name:",random_movie[1])
    print("Movie Language:",random_movie[2])
    print("Movie Genre:",random_movie[3])
    print("Release Year:",random_movie[4],"  ","IMDb Rating:",random_movie[5])
    print("IMDb Link:",random_movie[6])

while True:
    print("")
    ch=input("1.Create database(C)\n2.Add Movie Records(A)\n3.Edit Movie Records(E)\n4.Display All Movies(D)\n5.Browse Movies(B)\n6.Find a movie(F)\n7.Randomize(R)\n8.Quit(Q)\n9.Drop Database(Drop)\n")
    inp=ch.lower()
    if inp in ['c','1']:
        create()
    elif inp in ['a','2']:
        add()
    elif inp in ['e','3']:
        edit()
    elif inp in ['d','4']:
        display()
    elif inp in ['b','5']:
        browse()
    elif inp in ['f','6']:
        find()
    elif inp in ['r','7']:
        randomize()
    elif inp in ['q','8']:
        break
    elif inp in ['drop','9']:
        drop()
    else:
        print("")
        print("Invalid Input")
db.close()