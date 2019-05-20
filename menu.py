#!/usr/bin/env python3
# email: RMIT.PIOT.A2@gmail.com
# password: A2abc123

from validator import Validator
from database_utils import DatabaseUtils
from calendar import CalendarUtils
from validator import Validator
#from QR import QR
from voice_search import VoiceSearchUtils

from datetime import datetime, date, timedelta
import json
import time

BOOK_HEADERS = ["ISBN", "Title", "Author", "Year published"]
BORROW_HEADERS = ["BorrowID", "ISBN", "Username", "Borrow date", "Due date",
                  "Return date", "Event ID"]
DATE_FORMAT = "%Y-%m-%d"


class MasterApplication:
    """
    A class used to represent the Console Application on the Master Pi

    Attributes
    ----------
    username : string
        the username of the person logged in
    validator : Validator
        the link to the validator script
    QR : QR
        the link to the QR script
    calendar : CalendarUtils
        the link to the CalendarUtils script
    """

    def __init__(self, username):
        self.username = username
        self.validator = Validator()
        self.calendar = CalendarUtils()
        self.voice = VoiceSearchUtils()
        #self.QR = QR()

        with DatabaseUtils() as db:
            db.createBookTable()
            db.createBorrowTable()
            db.insertSampleBook()

        #self.showMenu()
        # this will be removed as the master socket script will intantiate and call this

    def voiceInput(self):
        translation = self.voice.voiceSearch()

        if(translation is None):
            print("Failed to get speech input.")
        else:
            print("Your search is:\t {}".format(translation))
            
        return translation

    def showMenu(self):
        """A function created to display the main menu"""

        print()
        print('-.-'*20)
        print("Welcome To the Library")
        print('-.-'*20)

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
                self.returnBookMenu()
            elif(selection == "D"):
                self.listBooks()
            elif(selection == "E"):
                self.listBorrowsByUser()
            elif(selection == "F"):
                print("Logged out")
                return 
                # In final submission, we return something here
                # Then exit back to master.py which will then send a message via the
                # socket to the reception pi saying that the current user has
                # logged out and that it is free to allow another user to login
            else:
                print("Invalid input - please try again.\n")

    def printList(self, subject, listName, headers, data):
        """
        A function created to print the searched for items in a list

        Args:
            subject: which database to get the data from
            listName: title to print
            headers:
            data: the list items

        """

        self.printSection(listName.upper())

        print("".join(["{:<30}".format(item) for item in headers]))

        if not data:
            print("No {} is found".format(subject))
            self.printEndSection()
            return False
        else:
            for row in data:
                print("".join(["{:<30}".format(str(item)) for item in row]))
            self.printEndSection()
            return True


    def printSection(self, sectionName):
        """
        A function created to print a section title

        Args:
            sectionName: title to print

        """

        print()
        print ('-'*100)
        print("\t"*5 + sectionName.upper())
        print ('-'*100)
        print()

    def printEndSection(self):
        """ A function created to print a message ending the section """

        print()
        print("-"*50 + "END" + "-"*50)
        print()

    def listBooks(self):
        with DatabaseUtils() as db:
            self.printList("books", "all books", BOOK_HEADERS, db.getBooks())

    def listBorrowsByUser(self):
        with DatabaseUtils() as db:
            self.printList(
                "user borrow records", "your borrow records", BORROW_HEADERS,
                db.getBorrowsByUsername(self.username))

    def searchBook(self):
        """A function created to print the main search menu options"""

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
                if(self.searchBookByISBN()):
                    self.wantsToBorrow()
            elif(selection == "B"):
                if(self.searchBookByAuthor()):
                    self.wantsToBorrow()
            elif(selection == "C"):
                if(self.searchBookByTitle()):
                    self.wantsToBorrow()
            elif(selection == "D"):
                break
            else:
                print("Invalid input - please try again.\n")

    def searchBookByISBN(self):
        """A function created to search for a book by ISBN"""

        self.printSection("SEARCH BY ISBN")

        isbn = input("ISBN: ")

        if self.validator.validateISBN(isbn):
            with DatabaseUtils() as db:
                return self.printList(
                    "search results", "all search results", 
                    BOOK_HEADERS, db.getBookByISBN(isbn))


    def searchBookByTitle(self):
        """A function created to search for a book by Title"""
        self.printSection("SEARCH BY TITLE")

        title = input("Title: ")

        if self.validator.validateTitle(title):
            with DatabaseUtils() as db:
                return self.printList(
                    "search results", "all search results", 
                    BOOK_HEADERS, db.getBooksByTitle(title))
 

    def searchBookByAuthor(self):
        """A function created to search for a book by Author"""
        
        self.printSection("SEARCH BY AUTHOR")

        author = input("Author: ")

        if self.validator.validateAuthor(author):
            with DatabaseUtils() as db:
                return self.printList(
                    "search results", "all search results", 
                    BOOK_HEADERS, db.getBooksByAuthor(author))
    
    def wantsToBorrow(self):
        while(True):
            print("Would you like to borrow one of these results? Y/N")
            print("Y) Yes")
            print("N) No, take me back to the search menu")

            selection = input("Select an option: ").upper()
            print()

            if(selection == "Y"):
                if(not self.borrowBook()):
                    break
            elif(selection == "N"):
                break
            else:
                print("Invalid input - please try again.\n")

    def borrowISBN(self, isbn):
        """
        A function created to borrow a book based on its ISBN

        Args:
            isbn: string of the isbn of the book looking to be borrowed

        """

        if self.validator.validateISBN(isbn):
            if self.validator.isbnExists(isbn):
                if self.validator.onLoan(self.username, isbn):
                    print("You can not borrow this book again.\n")
                else:
                    # currentdate = date.today()
                    # dueDate = currentdate + timedelta(days=7)
                    currentdate = datetime.now()
                    dueDate = currentdate.date() + timedelta(days=7)
                    
                    # #This Google Calendar function is not working!
                    # #Need to debug this
                    #eventID = self.calendar.createCalendarEvent(
                        dueDate.strftime(DATE_FORMAT), isbn, self.username)

                    #for now, use a hard-coded eventID
                    #eventID = 10000000

                    with DatabaseUtils() as db:
                        # made change here to create event then
                        # add the borrow with the eventID
                        
                        if(db.insertBorrow(isbn, self.username, eventID)):
                            print(
                                "Book ISBN {} sucessfully borrowed by {}."
                                .format(isbn, self.username))
                            print(
                                "Due date is: " + dueDate.strftime(
                                    DATE_FORMAT))
                            print("An event has been set in your Google Calendar")
                        else:
                            # #This Google Calendar function is not working!
                            # #Need to comment this out for now to test other functions
                            #self.calendar.removeCalendarEvent(eventid)
                            print("Book unsucessfully borrowed due to some db error")

    def borrowBook(self):
        """A function created to borrow a book"""

        runAgain = True

        while(runAgain):
            self.printSection("BORROW A BOOK")
            isbn = input("ISBN: ")
            self.borrowISBN(isbn)
            runAgain = self.repeatsFunction("borrow")
        
        return False
    def returnBook(self, isbn):
        """A function created to return a book based on its ISBN

        Args:
            isbn: string of the isbn of the book looking to be borrowed
        """
        if self.validator.validateISBN(isbn):
            if self.validator.isbnExists(isbn):
                if self.validator.onLoan(self.username, isbn):
                    with DatabaseUtils() as db:
                        if(db.updateReturnDate(isbn, self.username)):
                            print(
                                "Book ISBN {} sucessfully returned by {}."
                                .format(isbn, self.username))

                            # get id from database
                            eventString = db.getEventID(self.username, isbn)
                            # remove google calendar event
                            self.calendar.removeCalendarEvent(eventString)
                        else:
                            print(
                                "Book unsucessfully returned by {}"
                                .format(self.username))
                else:
                    print("You did not borrow Book ISBN {}".format(isbn))
                    print("Please return another book")

    def returnBookMenu(self):
        """A function created to print the main return menu options"""

        self.printSection("RETURN A BOOK")

        while(True):
            print("How would you like to return?")
            print("A) Return by ISBN")
            print("B) Return by QR Code")
            print("C) Return to main menu")
            selection = input("Select an option: ").upper()
            print()

            if(selection == "A"):
                self.returnBookISBN()
            elif(selection == "B"):
                print("Currently not implemented")
                #self.returnBookQR()
            elif(selection == "C"):
                break
            else:
                print("Invalid input - please try again.")

    def returnBookISBN(self):
        """A function created to return a book - by getting its ISBN"""

        runAgain = True

        while(runAgain):
            self.printSection("RETURN A BOOK")

            isbn = input("ISBN: ")
            self.returnBook(isbn)
            runAgain = self.repeatsFunction("return")

    def returnBookQR(self):
        """A function created to return a book - by getting the QR code"""

        runAgain = True

        while(runAgain):
            self.printSection("RETURN A BOOK")

            #isbn = self.QR.readQR()
            self.returnBook(isbn)
            runAgain = self.repeatsFunction("return")

    def repeatsFunction(self, action):
        """
        A function created to ask the user if they wish to repeat the action

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
                print("Invalid input - please try again.\n")

if __name__ == "__main__":
    app = MasterApplication("borrower1")
