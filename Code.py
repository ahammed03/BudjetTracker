# SQL QUERIES for tables

createTableQuery = '''create table if not exists user(
    serialnumber int auto_increment, 
    userid varchar(40) primary key ,
    name varchar(40),
    phone_number varchar(10) unique,
    income int ,
    password varchar(30)
    ,unique(serialnumber))'''

createTableQuery1='''create table if not exists user_data(  
    userid varchar(40) primary key , 
    category varchar(20), 
    subcategory varchar(20),
    amount int , 
    created_at datetime default current_timestamp )'''




class budjetTracker:


    def __init__(self) -> None:
        import mysql.connector     # My SQL  module is imported
        self.connector = mysql.connector.connect(
        host='localhost', # its just host , local host means local system 
        port='3306',  
        user='root',
        password=open(
            r"C:\Users\Ahammed\Desktop\my_sql_pass_key.txt", "r").readline(),
        database="main"
        )
        self.cursor = self.connector.cursor() 


    def Login(self):
        userName = input("Enter ur Username:-")
        password = input("Enter ur password:-")   # need to create forgot password option 
        # forgot password should be in below  mentioned format
        # create a random 4 digit number using random module 
        # add that number into database using user mobile number
        # send the 4 digit random nnumber to the user mail id or mobile
        # get input of 4 digit number from user if it matches update the password column or userid column of user by mobile number
        query = "select * from user where userid=%s and password=%s"
        self.cursor.execute(query,(userName,password))
        temp = self.cursor.fetchall()
        if not temp:
            choice=int(input("Enter 1 to Re attempt 0 to Sign up :-"))
            if choice==1:
                self.Login()
            elif choice==0:
                print("please sign up")
                self.signUpMethod()
        else:
            print("Login Sucessfull")
            # print(temp[0][:2])
            return self.menu(temp[0][:2])
        

    def menu(self,temp):
        choice=int(input('''\nChoose your option
1 : Add spendings       2 : update Income 
3 : Track spendings     4 : update profile
5 : Logout 
:-'''))
        if choice==1:
            self.addspendings(temp) 
        elif choice==2:
            while 1:
                try:
                    new_income=int(input("Enter your new monthly Income:-"))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid Income.")
            query='''update user set income=%s where userid=%s'''
            self.cursor.execute(query,(new_income,temp[1]))
            self.connector.commit()
            incomeInText=f'{new_income:,}'
            print("Your new Income :", incomeInText) 
            print("Income Updated")
            exit=int(input("Enter 0 to Go Back 1 to Exit"))
            if exit==1:
                return 
            elif exit==0:
                return self.menu(temp)
        elif choice==3:
            self.TrackSpendings(temp)
        elif choice==5:
            print("Thank You ")
            return
        elif choice==4:
            self.updateProfile(temp)
        else:
            return self.menu(temp)
                        

    def signUpMethod(self):

        def passwordchecker(password):
            conditions=[
                len(password)>=8,
                any(i.islower() for i in password),
                any(i.isupper() for i in password),
                any(i.isdigit() for i in password),
                any(i in "!@#$%^&*()_+-=[]|;:'<>,.?/" for i in password)
            ]
            return all(conditions)
        
        print("please fill the details..")
        name =input("Enter ur Name:-")
        while True:
            userName= input("create ur username:-")
            query="select * from user where userid = %s"
            self.cursor.execute(query,(userName,))
            temp=self.cursor.fetchall()
            if temp:
                print("username already taken, Try again")
            else:
                break

        phone_no = input("Enter ur mobile number:-") #need to execute query to check the number is already registered or not 
                                                     # need to check until the phone number should be  length l0 
        income = input("Enter ur monthly income:-")  # income greater than 0 
        while True:
            password=input('''\npassword should have length above 8 
password must contain a Upper case letter
password must contain a lower case letter
password must contain a digit 
password must contain any special characters like this ['!@#$%^&*()_+-=["1 : Vehicle Expenses","2 : Public Transportation:","3 : Rideshare Services"]|;:<>,.?/]\n
Enter your password:-''')
            if passwordchecker(password):
                break
            else:
                print("\nPlease create a valid password")
        query='''
                INSERT INTO user(userid,name,phone_number,income,password) VALUES(%s,%s,%s,%s,%s) '''
        self.cursor.execute(query,(userName,name,phone_no,income,password))
        self.connector.commit()
        print("Registration Sucessfull..")
        return  self.Login()
    

    def addspendings(self,temp):
        print('''\nWelcome to spendings section ''')
        userid=temp[1]
        while 1:
            try:
                user_input = int(input("Enter amount to add: "))
                print("You entered:", user_input)
                break
            except ValueError:
                print("Invalid input. Please enter a valid amount.")
        # category dictonary has the data of category of spending mainly the user can spend
        category={
            1:"Basic Needs",
            2:"Transportation",
            3:"Health Care",
            4:"Debt and Financial Obligations",
            5:"Entertainment and Leisure",
            6:"Education",
            7:"Personal Care and Well-being",
            8:"Miscellaneous"
        }
        while 1:
            try:
                category_input=int(input('''Choose ur category which u spend 
        1 : Basic Needs                     2 : Transportation
        3 : Health Care                     4 : Debt and Financial Obligations
        5 : Entertainment and Leisure       6 : Education
        7 : Personal Care and Well-being    8 : Miscellaneous
        :-'''))
                break
            except ValueError:
                print("\nInvalid input.\n")

        
        # sample dictionary is just a data which is used to particular data at subcategory input 
        sample={
            "Basic Needs": "  - 1: Housing\n  - 2: Food\n  - 3: Clothing and Apparel\n :-",
            "Transportation": "  - 1: Vehicle Expenses\n  - 2: Public Transportation\n  - 3: Rideshare Services\n :-",
            "Health Care": "  - 1: Medical Expenses\n  - 2: Fitness\n :-",
            "Debt and Financial Obligations": "  - 1: Loans\n  - 2: Savings and Investments\n :-",
            "Entertainment and Leisure": "  - 1: Entertainment\n  - 2: Hobbies\n  - 3: Vacation and Travel\n :-",
            "Education": "  - 1: Tuition and Fees\n  - 2: Books and Supplies\n :-",
            "Personal Care and Well-being": "  - 1: Toiletries\n  - 2: Salon and Spa\n :-",
            "Miscellaneous": "  - 1: Pet Expenses\n  - 2: Taxes\n  - 3: Gifts and Celebrations\n :-"
        }  
        # sub categories dictonary is a data which is under as sub categories of main categories which is used to push into database         
        sub_categories = {
                "Basic Needs": {
                    1: "Housing",
                    2: "Food",
                    3: "Clothing and Apparel",
                },
                "Transportation": {
                    1: "Vehicle Expenses",
                    2: "Public Transportation",
                    3: "Rideshare Services",
                },
                "Health Care": {
                    1: "Medical Expenses",
                    2: "Fitness",
                },
                "Debt and Financial Obligations": {
                    1: "Loans",
                    2: "Savings and Investments",
                },
                "Entertainment and Leisure": {
                    1: "Entertainment",
                    2: "Hobbies",
                    3: "Vacation and Travel",
                },
                "Education": {
                    1: "Tuition and Fees",
                    2: "Books and Supplies",
                },
                "Personal Care and Well-being": {
                    1: "Toiletries",
                    2: "Salon and Spa",
                },
                "Miscellaneous": {
                    1: "Pet Expenses",
                    2: "Taxes",
                    3: "Gifts and Celebrations",
                },
            }
        while 1:
            try:
                sub_category_input=int(input(sample[category[category_input]]))
                userchoice=sub_categories[category[category_input]][sub_category_input]
                print("You choose :",userchoice)
                break 
            except ValueError:
                print("Invalid Input")
        query='''insert into user_data (userid,category,subcategory,amount) values (%s,%s,%s,%s)'''
        self.cursor.execute(query,(userid,category[category_input],userchoice,user_input))
        self.connector.commit()
        print("Sucessfully added spending")
        extra=input('''Press 1 to enter more, press 0 to exit
:-''')
        if extra=="1":
            self.addspendings(temp)
        return self.menu(temp)
    

    def TrackSpendings(self,temp):   #THis function for to get every month how much we spend on which category
        details=temp[1]
        while 1:
            try:
                choice=int(input('''
Spendings of Particular
1  :  Yearly
2  :   Monthly
3  :   Day
Enter :-'''))
                break
            except ValueError:
                print("Invalid Input")
        date=input('''Enter space for each date month and year
Like this :  (YYYY MM DD)   : 2023 10 25
Enter Date ''').split()
        if choice==1:
            year=date[0]
            query= '''SELECT  category,SUM(amount)  
                    FROM user_data 
                    WHERE userid=%s  AND YEAR(created_at)=%s 
                    GROUP BY category'''
            self.cursor.execute(query,(details,year))
            result=self.cursor.fetchall()
        elif choice==2:
            year=date[0]
            month=date[1]
            query='''
                    SELECT  category,SUM(amount)  
                    FROM user_data 
                    WHERE userid=%s AND MONTH(created_at)=%s AND YEAR(created_at)=%s 
                    GROUP BY category'''
            self.cursor.execute(query,(details,month,year))
            result=self.cursor.fetchall()
        elif choice==3:
            year=date[0]
            month=date[1]
            day=date[2]
            query = '''
                    SELECT  category,SUM(amount)  
                    FROM user_data 
                    WHERE userid=%s AND DAY(created_at)=%s AND  MONTH(created_at)=%s AND YEAR(created_at)=%s 
                    GROUP BY category'''
            self.cursor.execute(query,(details,day,month,year))
            result=self.cursor.fetchall()
        total=0
        self.cursor.execute('select income from user where userid=%s',(details,))
        Income=self.cursor.fetchall()[0][0]
        if choice==1:
            Income=Income*12
        Income1=Income
        Income1=f'{Income1:,}'

        print("Income:",Income1)
        print('''          Your Total Spendings       ''')
        for i in range(len(result)):
            print(f'{result[i][0]:<30}: {result[i][1]:<10} ({(int(result[i][1])/Income*100):.2f} % of Income)')
            total+=result[i][1]
        print("-"*35)
        print(f"You Spent                    : {total}")
        if ((total/Income)* 100) >100:
            print(f'You spent {((total/Income)*100):.2f}% more than what u Earn')
        else:
            print(f'You spent {(total/Income)*100:.2f}% of {Income}')  
        exit = int(input("Enter 0 to Go back  1 to Exit :-"))    
        if exit==1:
            return 
        elif exit==0:  
            return self.menu(temp)
        

    def updateProfile(self,temp):
        userid=temp[1]
        print("you can only change phone number and Name, changing of other will available sooon...")
        nameOrMobileNumber=int(input('''Enter 1 to change only name
Enter 2 to change Mobile
Enter 3 to change Both
Enter 0 to Go Back to Main Menu
:-'''))
        if nameOrMobileNumber==1:
            name=input("Enter ur New name:-")
            query='''UPDATE USER SET name=%s WHERE userid=%s'''
            self.cursor.execute(query,(name,userid))
            self.connector.commit()
            print("Profile Updated")
            return self.menu(temp)
        elif nameOrMobileNumber==2:
            mobileNumber=input("Enter ur New Mobile Number:-")
            query='''UPDATE USER SET phone_number=%s WHERE userid=%s'''
            self.cursor.execute(query,(mobileNumber,userid))
            self.connector.commit()
            print("Profile Updated")
            return self.menu(temp)
            
        elif nameOrMobileNumber==3:
            name=input("Enter ur New name:-")
            mobileNumber=input("Enter ur New Mobile Number:-")
            query='''UPDATE USER SET name=%s AND phone_number=%s WHERE userid=%s'''
            self.cursor.execute(query,(name,mobileNumber,userid))
            self.connector.commit()
            print("Profile Updated")
            return self.menu(temp)
        
        elif nameOrMobileNumber==0:
            return self.menu(temp)






                
instanceOfBudjecttrcaker=budjetTracker()
instanceOfBudjecttrcaker.Login()
# instanceOfBudjecttrcaker.TrackSpendings('ahammed03')


