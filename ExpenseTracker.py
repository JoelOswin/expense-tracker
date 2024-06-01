#!/usr/bin/env python3
import sqlite3
from datetime import datetime

class ExpenseTracker():
    def __init__(self):
        self.months_dict={
            1:"jan",
            2:"feb",
            3:"mar",
            4:"april",
            5:"may",
            6:"june",
            7:"july",
            8:"aug",
            9:"sept",
            10:"oct",
            11:"nov",
            12:"dec"
        }
        self.connection=sqlite3.connect('expense.db')
        self.cursor=self.connection.cursor()
        self.month=int(datetime.now().month)
        print(self.months_dict[self.month])
        try:
            self.cursor.execute(f"CREATE TABLE {self.months_dict[self.month]}(SLNO integer Primary Key,Spent_on char(25), Expense int(20))")
            print("Successfully created table")        
        except sqlite3.OperationalError:
            print("Table already exists")
            pass
        
        try:
            self.cursor.execute("CREATE TABLE budget(Month char(25),Budget integer)")
            print("Successfully created table")        
        except sqlite3.OperationalError:
            print("Table already exists")
            pass

        #self.cursor.execute(f"INSERT INTO budget VALUES('{self.months_dict[self.month]}',10)")
        result=self.cursor.execute("SELECT * FROM budget")

        for row in result:
            print(row)
            if row is not None:
                #self.setBudget(10)
                self.budget=10
            else:
                if self.months_dict[self.month] in row:
                    _,self.budget=row
                    #self.setBudget(self.budget)

        try:
            self.isExceeded()
        except (sqlite3.OperationalError,TypeError):
            print("No Data was added")
            pass
    


    def add_expense(self,item:str,price:int):
        print(f"INSERT INTO {self.months_dict[self.month]} (Spent_on,Expense) VALUES('{item}',{price})")
        self.cursor.execute(f"INSERT INTO {self.months_dict[self.month]} (Spent_on,Expense) VALUES('{item}',{price})")
        self.PrintAllRows()
        self.isExceeded()



    def isExceeded(self):
        total_expense=self.cursor.execute(f"SELECT SUM(Expense) FROM {self.months_dict[self.month]}")
        for row in total_expense:
            for r in row:
                self.expense=r
            print(self.expense)
        if self.expense>self.budget:
            self.RaiseAlert()



    def PrintAllRows(self):
        allrows=[]
        result=self.cursor.execute(f"SELECT * FROM {self.months_dict[self.month]}")
        for row in result:
            print(row)
            allrows.append(allrows)
        return allrows



    def RaiseAlert(self):
        print("Budget Exceeded!")



    def setBudget(self,budget:int):
        self.cursor.execute(f"INSERT INTO budget VALUES('{self.months_dict[self.month]}',{budget})")



    def __del__(self):
        self.connection.commit()
        self.connection.close()
    
