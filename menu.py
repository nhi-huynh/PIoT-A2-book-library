#!/usr/bin/env python3

from database_utils import DatabaseUtils
from validator import Validator
from datetime import datetime, date, timedelta
import json
import time

BOOK_HEADERS = ["ISBN", "Title", "Author", "Year published"]
BORROW_HEADERS = ["ISBN", "Username", "Borrow date", "Due date", "Return date"] 
DATE_FORMAT = "%Y-%m-%d"


class MasterApplication:

    def __init__(self, username):
        self.username = username
        self.validator = Validator()

        with DatabaseUtils() as db:
            db.createBookTable()
            db.createBorrowTable()
            db.insertSampleBook()   
        
        self.showMenu()

    def showMenu(self):
        print()
        print ('-.-'*20)
        print("Welcome To the Library")
        print ('-.-'*20)
        
        while(True):
            print()
            print ('-.-'*20)
            print("What would you like to do today?")
            print ('-.-'*20)
            print()
            print("(A) Search a Book")
            print("(B) Borrow a Book")
            print("(C) Return a Book")
            print("(D) List all Books")
            print("(E) List your Borrow records")
            print("(F) Log out")

            selection = input("Select an option: ").upper()

            if(selection == "A"):
                self.searchBook()
            elif(selection == "B"):
                self.borrowBook()
            elif(selection == "C"):
                self.returnBook()
            elif(selection == "D"):
                self.listBooks()
            elif(selection == "E"):
                self.listBorrowsByUser()
            elif(selection == "F"):
                print("Logged out")
                break
            else:
                print("Invalid input - please try again.")

    def printList(self, subject, listName, headers, data):
        self.printSection(listName.upper())
        
        print("".join(["{:<25}".format(item) for item in headers]))

        if not data:
            print("No {} is found".format(subject))
        else:
            for row in data:
                print("".join(["{:<25}".format(str(item)) for item in row]))
        print()
        print("-"*50 + "END" + "-"*50)
        print()
    
    def printSection(self, sectionName):
        print()
        print ('-'*100)
        print("\t"*5 + sectionName.upper())
        print ('-'*100)
        print()
            
    def listBooks(self):
        with DatabaseUtils() as db:
            self.printList("books", "all books", BOOK_HEADERS, db.getBooks())
                
    def listBorrowsByUser(self):
        with DatabaseUtils() as db:
            self.printList("user borrow records", "your borrow records", BORROW_HEADERS, db.getBorrowsByUsername(self.username))

    # def listBorrows(self):
    #     BOOK_HEADERS = ["ISBN", "Username", "Borrow date", "Due date", "Return date"] 
    #     with DatabaseUtils() as db:
    #         self.printList("borrow records", "all borrow records", BOOK_HEADERS, db.getBorrows())

    def searchBook(self):
        self.printSection("SEARCH FOR A BOOK")

        while(True):
            print("How would you like to search?")
            print("A) Search by ISBN")
            print("B) Search by Author Name")
            print("C) Search by Book Title")
            print("D) Return to main menu")
            selection = input("Select an option: ").upper()
            print()

            if(selection == "A"):
                self.searchBookByISBN()
            elif(selection == "B"):
                self.searchBookByAuthor() 
            elif(selection == "C"):
                self.searchBookByTitle()
            elif(selection == "D"):
                break
            else:
                print("Invalid input - please try again.")

    def searchBookByISBN(self):
        self.printSection("SEARCH BY ISBN")

        isbn = input("ISBN: ")

        if self.validator.validateISBN(isbn):
            with DatabaseUtils() as db:
                self.printList("search results", "all search results", BOOK_HEADERS, db.getBookByISBN(isbn))

    def searchBookByTitle(self):
        self.printSection("SEARCH BY TITLE")

        title = input("Title: ")

        if self.validator.validateTitle(title):
            with DatabaseUtils() as db:
                self.printList("search results", "all search results", BOOK_HEADERS, db.getBooksByTitle(title))

    def searchBookByAuthor(self):
        self.printSection("SEARCH BY AUTHOR")

        author = input("Author: ")

        if self.validator.validateAuthor(author):
            with DatabaseUtils() as db:
                self.printList("search results", "all search results", BOOK_HEADERS, db.getBooksByAuthor(author))

    def borrowBook(self):
        runAgain = True
        
        while(runAgain):
            self.printSection("BORROW A BOOK")

            isbn = input("ISBN: ")
            if self.validator.validateISBN(isbn):
                if self.validator.isbnExists(isbn):
                    if self.validator.onLoan(self.username, isbn):
                        print("You can not borrow this book again until you return it to the library.")
                        print("Please borrow another book")
                    else:
                        currentdate = date.today()
                        dueDate = currentdate + timedelta(days=7)
                        with DatabaseUtils() as db:
                            if(db.insertBorrow(isbn, self.username)):
                                print("Book ISBN {} sucessfully borrowed by {}.".format(isbn, self.username))
                                print("Due date is: " + dueDate.strftime(DATE_FORMAT))
                            else:
                                print("Book ISBN {} unsucessfully borrowed by {}.".format(isbn, self.username))
            runAgain = self.repeatsFunction("borrow")
        
    def returnBook(self):
        runAgain = True
        
        while(runAgain):
            self.printSection("RETURN A BOOK")

            isbn = input("ISBN: ")
            if self.validator.validateISBN(isbn):
                if self.validator.isbnExists(isbn):
                    if self.validator.onLoan(self.username, isbn):
                        with DatabaseUtils() as db:
                            if(db.updateReturnDate(isbn, self.username)):
                                print("Book ISBN {} sucessfully returned by {}.".format(isbn, self.username))
                            else:
                                print("Book ISBN {} unsucessfully returned by {}.".format(isbn, self.username))  
                    else:
                        print("You did not borrow Book ISBN {}".format(isbn))
                        print("Please return another book")
            runAgain = self.repeatsFunction("return")
                        
    def repeatsFunction(self, action):
        while True:
            print()
            print("Would you want to {} another book?".format(action))
            answer = input("Y/N?: ").upper()
            
            if answer == "Y":
                return True
            elif answer == "N":
                return False
            else:
                print("Invalid input - please try again.")
        
if __name__ == "__main__":
    app = MasterApplication("borrower1")
