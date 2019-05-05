#!/usr/bin/env python3
# email: RMIT.PIOT.A2@gmail.com
# password: A2abc123

from database_utils import DatabaseUtils
from calendar import *
from validator import Validator
from datetime import datetime, date, timedelta
import json
import time

BOOK_HEADERS = ["ISBN", "Title", "Author", "Year published"]
BORROW_HEADERS = ["ISBN", "Username", "Borrow date", "Due date", "Return date"]
DATE_FORMAT = "%Y-%m-%d"


class MasterApplication:
    """
    A class used to represent the Console Application on the Master Pi

    Attributes
    ----------
    username : string
        the username of the person logged in
    validator : Validator
        the

    Methods
    -------
    showMenu()
        A fuction created to display the main menu
    printList(subject, listName, headers, data):
        A fuction created to print the searched for items in a list
    printSection(sectionName):
        A fuction created to print a section
    listBooks():
    listBorrowsByUser():
    searchBook():
        A fuction created to print the main search menu options
    searchBookByISBN():
        A fuction created to search for a book by ISBN
    searchBookByTitle():
        A fuction created to search for a book by Title
    searchBookByAuthor():
        A fuction created to search for a book by Author
    borrowISBN(isbn):
        A fuction created to borrow a book based on its ISBN
    borrowBook():
        A fuction created to borrow a book
    returnBook():
        A fuction created to return a book
    repeatsFunction(action):
        A fuction created to ask the user if they wish to repeat the action

    """

    def __init__(self, username):
        self.username = username
        self.validator = Validator()

        with DatabaseUtils() as db:
            db.createBookTable()
            db.createBorrowTable()
            db.insertSampleBook()

        self.showMenu()

    def showMenu(self):
        """
        A fuction created to display the main menu

        Args:

        Returns:
        """

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
            print("(F) Logout")

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
                # return
                # exit back to master.py which will then send a message via the
                # socket to the reception pi saying that the current user has
                # logged out and that it is free to allow another user to login
            else:
                print("Invalid input - please try again.")

    def printList(self, subject, listName, headers, data):
        """
        A fuction created to print the searched for items in a list

        Args:
            subject: which database to get the data from
            listName: title to print
            headers:
            data: the list items

        Returns:
        """

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
        """
        A fuction created to print a section

        Args:
            sectionName: title to print

        Returns:
        """

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
            self.printList(
                "user borrow records", "your borrow records", BORROW_HEADERS,
                db.getBorrowsByUsername(self.username))

    # def listBorrows(self):
    #     BOOK_HEADERS = [
    # "ISBN", "Username", "Borrow date", "Due date", "Return date"]
    #     with DatabaseUtils() as db:
    #         self.printList(
    # "borrow records", "all borrow records", BOOK_HEADERS, db.getBorrows())

    def searchBook(self):
        """
        A fuction created to print the main search menu options

        Args:

        Returns:
        """

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
        """
        A fuction created to search for a book by ISBN

        Args:

        Returns:
        """

        self.printSection("SEARCH BY ISBN")

        isbn = input("ISBN: ")

        if self.validator.validateISBN(isbn):
            with DatabaseUtils() as db:
                self.printList(
                    "search results", "all search results",
                    BOOK_HEADERS, db.getBookByISBN(isbn))
                answer = input(
                    "Would you like to borrow based one of these books? Y/N"
                    ).upper()
                if answer is 'Y':
                    # get isbn
                    isbn = input("Which isbn would you like to borrow?")
                    self.borrowFromSearch(isbn)

    def searchBookByTitle(self):
        """
        A fuction created to search for a book by Title

        Args:

        Returns:
        """

        self.printSection("SEARCH BY TITLE")

        title = input("Title: ")

        if self.validator.validateTitle(title):
            with DatabaseUtils() as db:
                self.printList(
                    "search results", "all search results",
                    BOOK_HEADERS, db.getBooksByTitle(title))
                answer = input(
                    "Would you like to borrow based one of these books? Y/N"
                    ).upper()
                if answer is 'Y':
                    # get isbn
                    isbn = input("Which isbn would you like to borrow?")
                    self.borrowFromSearch(isbn)

    def searchBookByAuthor(self):
        """
        A fuction created to search for a book by Author

        Args:

        Returns:
        """

        self.printSection("SEARCH BY AUTHOR")

        author = input("Author: ")

        if self.validator.validateAuthor(author):
            with DatabaseUtils() as db:
                self.printList(
                    "search results", "all search results",
                    BOOK_HEADERS, db.getBooksByAuthor(author))
                answer = input(
                    "Would you like to borrow based one of these books? Y/N"
                    ).upper()
                if answer is 'Y':
                    # get isbn
                    isbn = input("Which isbn would you like to borrow?")
                    self.borrowFromSearch(isbn)

    def borrowISBN(self, isbn):
        """
        A fuction created to borrow a book based on its ISBN

        Args:
            isbn: string of the isbn of the book looking to be borrowed

        Returns:
        """

        if self.validator.validateISBN(isbn):
                if self.validator.isbnExists(isbn):
                    if self.validator.onLoan(self.username, isbn):
                        print("You can not borrow this book again.")
                    else:
                        currentdate = date.today()
                        dueDate = currentdate + timedelta(days=7)
                        with DatabaseUtils() as db:
                            # made change here to create event then
                            # add the borrow with the eventID
                            eventid = self.calendar.createCalendarEvent(
                                dueDate.strftime(DATE_FORMAT), isbn)
                            if(db.insertBorrow(isbn, self.username, eventid)):
                                print(
                                    "Book ISBN {} sucessfully borrowed by {}."
                                    .format(isbn, self.username))
                                print(
                                    "Due date is: " + dueDate.strftime(
                                        DATE_FORMAT))
                            else:
                                self.calendar.removeCalendarEvent(eventid)
                                print("Book unsucessfully borrowed by")

    def borrowBook(self):
        """
        A fuction created to borrow a book

        Args:

        Returns:
        """

        runAgain = True

        while(runAgain):
            self.printSection("BORROW A BOOK")

            isbn = input("ISBN: ")
            self.borrowISBN(isbn)
            runAgain = self.repeatsFunction("borrow")

    def returnBook(self):
        """
        A fuction created to return a book

        Args:

        Returns:
        """

        runAgain = True

        while(runAgain):
            self.printSection("RETURN A BOOK")

            isbn = input("ISBN: ")
            if self.validator.validateISBN(isbn):
                if self.validator.isbnExists(isbn):
                    if self.validator.onLoan(self.username, isbn):
                        with DatabaseUtils() as db:
                            if(db.updateReturnDate(isbn, self.username)):
                                print(
                                    "Book ISBN {} sucessfully returned by {}."
                                    .format(isbn, self.username))

                                # get id from database
                                eventString = db.getEventID(username, isbn)
                                # remove google calendar event
                                self.calendar.removeCalendarEvent(eventString)
                            else:
                                print(
                                    "Book unsucessfully returned by {}"
                                    .format(self.username))
                    else:
                        print("You did not borrow Book ISBN {}".format(isbn))
                        print("Please return another book")
            runAgain = self.repeatsFunction("return")

    def repeatsFunction(self, action):
        """
        A fuction created to ask the user if they wish to repeat the action

        Args:
            action: borrow or return - action to be repeated if required

        Returns:
            True or False
        """

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
