import mysql.connector
mydb1=mysql.connector.connect(host='localhost',user='root',passwd='123456')
mycursor1=mydb1.cursor()
mycursor1.execute('create database if not exists ARS')

mydb=mysql.connector.connect(host='localhost',user='root',passwd='123456',database='ars')
mycursor=mydb.cursor()

try:
    mycursor.execute('create table credientials(Name varchar(20) not null, password varchar(20) not null, username varchar(20) primary key not null)')
    print()
except:
    print()

p=0
            
def start():
    global p
    print("Account Settings".center(150))
    opt= input("   1.Login\n   2.Sign-up\n   3.Change name\n   4.Change username\n   5.Go back\nenter your choice number:")
    if opt=='1':
        username = input("Enter your username:")
        password = input("Enter the password:")
        mycursor.execute("select Name from credientials where username='"+username+"'")
        myrecords=mycursor.fetchall()
        if myrecords==[]:
            print('Account not found'.center(150))
        else:
            for x in myrecords:
                for y in x:
                    name=y
                    print(('Successfully logged in as '+name+'.').center(150))
                    p=1
    elif opt=='2':
        print("Please remember the details you input here".center(150))
        name = input("Enter your full name:")
        p=input("Enter the password:")
        username=input('Please enter a username consisting of alphabets and digits:')
        t="Insert into credientials values('"+name+"','"+p+"','"+username+"')"
        mycursor.execute(t)
        mydb.commit()
        print('Account successfully created and logged in'.center(150))
        p=1
    elif opt=='3':
        user=input("Please enter your username:")
        password=input("Enter password:")
        name=input("Enter your new name:")
        mycursor.execute("update credientials set Name='"+name+"' where password='"+password+"'")
        mydb.commit()
        print("Name changed".center(150))
    elif opt=='4':
        name=input("Enter your name:")
        password=input("Enter password:")
        user=input("Enter new username:")
        mycursor.execute("update credientials set username='"+user+"' where password='"+password+"'")
        mydb.commit()
        print("Username changed".center(150))
    elif opt=='5':
        program()
    else:
        print('Invalid option'.center(150))
        program()


def bookflight():
    try:
        mycursor.execute("create table passengername(Full_name varchar(20),Airlines varchar(20),Departure_airport varchar(20),Arrival_airport varchar(20),Departure_date varchar(10),return_date varchar(10) default 'Nil',Class varchar(10),Status varchar(20),CodeNo varchar(4))")
        print('Please provide the following details for your Flight.......'.center(150))
    except:
        print('Please provide the following details for your Flight.......'.center(150))

    FullName=input('Enter your full name: ')
    departure_airport=input('enter airport of Departure: ')
    arrival_airport=input('enter airport of Arrival: ')
    departure_date=input('enter date of departure[YYYY-MM-DD]: ')
    option=input('Would you like a return ticket as well?[y/n] ')
    if option=='y':
        return_date=input('enter date of return [YYYY-MM-DD]: ')
    passengers=int(input('enter no.of co-passengers(excluding yourself): '))
    Class=input('enter ticket class[Economy/Business/First]: ')
    print()

    try:
        mycursor.execute("create table airlines(S_no int(3) primary key,Airlines varchar(50),Price int(5))")
        mycursor.execute('insert into airlines values(1,"Emirates",250)')
        mycursor.execute('insert into airlines values(2,"Air India",150)')
        mycursor.execute('insert into airlines values(3,"Qatar Airways",270)')
        mycursor.execute('insert into airlines values(4,"British Airways",300)')
        mycursor.execute('insert into airlines values(5,"United Airlines",280)')
        mycursor.execute('insert into airlines values(6,"Gulf Air",250)')
        mydb.commit()
        print('Here are the available Airlines:')
    except:
        print('Here are the available Airlines:')

    mycursor.execute('select * from airlines')
    from tabulate import tabulate
    print(tabulate(mycursor, headers=['S.no','Airlines','Price'],tablefmt="grid"))
    airline=input('Choose your Airline: ')
    mycursor.execute('select price from airlines where Airlines="'+airline+'"')
    for x in mycursor:
        for i in x:
            price=i
    import random
    code=random.randint(100,1000)
    #the following try-except block is used when the user does not input a return date
    try:
        mycursor.execute("insert into passengername values('"+FullName+"','"+airline+"','"+departure_airport+"','"+arrival_airport+"','"+departure_date+"','"+return_date+"','"+Class+"','Not checked-in','"+str(code)+"')")
        mydb.commit()
    except:
        mycursor.execute("insert into passengername values('"+FullName+"','"+airline+"','"+departure_airport+"','"+arrival_airport+"','"+departure_date+"','Nil','"+Class+"','Not checked-in','"+str(code)+"')")
        mydb.commit()
    for n in range(passengers):
        name=input('Enter next co-passenger name: ')
        try:
            mycursor.execute("insert into passengername values('"+name+"','"+airline+"','"+departure_airport+"','"+arrival_airport+"','"+departure_date+"','"+return_date+"','"+Class+"','Not checked-in','"+str(code)+"')")
            mydb.commit()
        except:
            mycursor.execute("insert into passengername values('"+name+"','"+airline+"','"+departure_airport+"','"+arrival_airport+"','"+departure_date+"','Nil','"+Class+"','Not checked-in','"+str(code)+"')")
            mydb.commit()
            
    print('You shall now be asked your payment details'.center(150))
    mode=input('enter card type [credit/debit]: ')
    cardno=int(input('enter card number: '))
    expdate=input('enter expiry date: ')
    cvv=int(input('enter cvv code: '))
    print('You are about to pay BD',price*(passengers+1),'for your flight ticket(s)')
    choice=input('Please confirm by entering "I Agree": ')
    if choice=='I Agree':
        print('Please wait while we process the transaction....'.center(150))
        print()
        print('Payment Received!!!'.center(150))
        print()
        print('Here is your Booking Confirmation:'.center(150))
        mycursor.execute('select * from passengername where CodeNo="'+str(code)+'"')
        from tabulate import tabulate
#the following print statement executes perfectly when the zoom size in IDLE=10
#if the zoom size is not 10, then the alignment of the print statement gets messed up
        print(tabulate(mycursor, headers=['Full Name','Airlines','Departure Airport','Arrival Airport','Departure date','Return date','Class','Status','CodeNo'],tablefmt="grid"))
        print()

    else:
        option=input('You did not agree to our terms and conditions. Would you like to cancel the transaction?[y/n]')
        if option==y:
            mycursor.execute('delete from passengername where CodeNo="'+str(code)+'"')
            print('Transaction cancelled.'.center(150))
        else:
            print('For security reasons, we are now redirecting you to the homepage.'.center(150))
            mycursor.execute('delete from passengername where CodeNo="'+str(code)+'"')
            bookflight()


def checkin():
    d=input("enter code received in Booking confirmation:")
    mycursor.execute("update passengername set Status='checked-in' where CodeNo='"+d+"'")
    mydb.commit()
    mycursor.execute("select * from passengername where CodeNo='"+d+"'")
    myrecords=mycursor.fetchall()
    if myrecords==[]:
        print("given details are invalid. Please try again".center(150))
        checkin()
    else:
        from tabulate import tabulate
        print(tabulate(myrecords, headers=['Full Name','Airlines','Departure Airport','Arrival Airport','Departure date','Return date','Class','Status','CodeNo'],tablefmt="grid"))
        print()
        print("checked in successfully".center(150))

def a():
    d=input("enter code received in Booking confirmation:")
    i=input("enter new arrival destination")
    b=("update passengername set Arrival_airport='"+i+"' where CodeNo='"+d+"'")
    mycursor.execute(b)
    mydb.commit()
    mycursor.execute("select * from passengername where CodeNo='"+d+"'")
    from tabulate import tabulate
    print(tabulate(mycursor, headers=['Full Name','Airlines','Departure Airport','Arrival Airport','Departure date','Return date','Class','Status','CodeNo'],tablefmt="grid"))
    print()
    
def d():
    d=input("enter code received in Booking confirmation:")
    i=input("enter new departure destination:")
    b=("update passengername set Departure_airport='"+i+"' where CodeNo='"+d+"'")
    mycursor.execute(b)
    mydb.commit()
    mycursor.execute("select * from passengername where CodeNo='"+d+"'")
    from tabulate import tabulate
    print(tabulate(mycursor, headers=['Full Name','Airlines','Departure Airport','Arrival Airport','Departure date','Return date','Class','Status','CodeNo'],tablefmt="grid"))
    print()
def t():
    d=input("enter code received in Booking confirmation:")
    choice=input('Do you want to change date of Departure or Return?:')
    if choice=='Departure' or choice=='departure':
        i=input("enter new date:")
        b=("update passengername set Departure_date='"+i+"' where CodeNo='"+d+"'")
        mycursor.execute(b)
        mydb.commit()
        mycursor.execute("select * from passengername where CodeNo='"+d+"'")
        from tabulate import tabulate
        print(tabulate(mycursor, headers=['Full Name','Airlines','Departure Airport','Arrival Airport','Departure date','Return date','Class','Status','CodeNo'],tablefmt="grid"))
        print()
    else:
        i=input("enter new date:")
        b=("update passengername set return_date='"+i+"' where CodeNo='"+d+"'")
        mycursor.execute(b)
        mydb.commit()
        mycursor.execute("select * from passengername where CodeNo='"+d+"'")
        from tabulate import tabulate
        print(tabulate(mycursor, headers=['Full Name','Airlines','Departure Airport','Arrival Airport','Departure date','Return date','Class','Status','CodeNo'],tablefmt="grid"))
        print()

def manage_booking():
    print("Manage your booking".center(150))
    ch=int(input("   1.change arrival venue\n   2.change departure venue\n   3.change date of travel\n   4.Check In\n   5.Go back\nenter your choice number:"))
    if ch==1:
        a()
        print("change completed successfully".center(150))
    if ch==2:
        d()
        print("change completed successfully".center(150))
    if ch==3:
        t()
        print("change completed successfully".center(150))
    if ch==4:
        checkin()
    if ch==5:
        program()

def display():
    code=int(input('Pease enter the code you received while booking the ticket:'))
    mycursor.execute('select * from passengername where CodeNo="'+str(code)+'"')
    from tabulate import tabulate
    print(tabulate(mycursor, headers=['Full Name','Airlines','Departure Airport','Arrival Airport','Departure date','Return date','Class','Status','CodeNo'],tablefmt="grid"))
    print()

def program():
    while True:
        print("Main Menu".center(150))
        print('   1.Account\n   2.Book flight\n   3.Manage Booking\n   4.Display Ticket\n   5.Exit System')
        ans=int(input('Enter your choice number:'))
        if ans==1:
            start()
            print(p)
        elif ans==2:
            if p==1:
                bookflight()
            else:
                print("Sorry. You cannot use this feature without logging in or signing up".center(150))
        elif ans==3:
            if p==1:
                manage_booking()
            else:
                print("Sorry. You cannot use this feature without logging in or signing up".center(150))
        elif ans==4:
            if p==1:
                display()
            else:
                print("Sorry. You cannot use this feature without logging in or signing up".center(150))
        elif ans==5:
            print('Thank you for visiting.'.center(150))
            break
        else:
            print('Invalid choice'.center(150))
            
print("Welcome to Airline Reservation System".center(150))
print()
program()
