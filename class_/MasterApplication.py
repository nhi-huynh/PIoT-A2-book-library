from class_.Validator import Validator
from class_.DatabaseUtils import DatabaseUtils
from class_.CalendarUtils import CalendarUtils
from class_.Validator import Validator
from class_.QR import QR
from class_.VoiceSearchUtils import VoiceSearchUtils
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

    Attributes:
        username : string
            the username of the person logged in
        validator : Validator
            the link to the validator script
        calendar : CalendarUtils
            the link to the CalendarUtils script
        QR : QR
            the link to the QR script
        voice : VoiceSearchUtils
            the link to the VoiceSearchUtils script
    """

    def __init__(self, username, config):
        self.username = username
        self.validator = Validator()
        self.calendar = CalendarUtils(config['gc']['credentials_path'])
        self.voice = VoiceSearchUtils()
        self.QR = QR()

        with DatabaseUtils() as db:
            db.createBookTable()
            db.createBorrowTable()
            db.insertSampleBook()

    def voiceInput(self):
        """
        A function created to get voice input from the user

        Returns:
            translation, string returned from voice search
        """

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
            else:
                print("Invalid input - please try again.\n")

    def printList(self, subject, listName, headers, data):
        """
        A function created to print the searched for items in a list

        Args:
            subject: which database to get the data from
            listName: title to print
            headers: header to print under
            data: the list items

        Returns:
            True if data is found
            False if no data is found
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
        """A function to list the books"""
        with DatabaseUtils() as db:
            self.printList("books", "all books", BOOK_HEADERS, db.getBooks())

    def listBorrowsByUser(self):
        """A function to list the books borrowed by the user"""
        with DatabaseUtils() as db:
            self.printList(
                "user borrow records", "your borrow records", BORROW_HEADERS,
                db.getBorrowsByUsername(self.username))

    def getSearchInput(self, item):
        """
        A function created to print the methods available to search

        Args:
            item: string stating what the input wants

        Returns:
            string of what the user is looking for
            or None
        """

        while(True):
            print("How would you like to search?")
            print("A) Voice input")
            print("B) Keyboard input")
            print("C) Return to main menu")
            selection = input("Select an option: ").upper()
            print()

            if(selection == "A"):
                return self.voiceInput()
            elif(selection == "B"):
                return input(item)
            elif(selection == "C"):
                return None
            else:
                print("Invalid input - please try again.")

    def searchBook(self):
        """A function created to print the main search menu options"""

        self.printSection("SEARCH FOR A BOOK")

        while(True):
            print("How would you like to search?")
            print("A) Search by ISBN")
            print("B) Search by Author Name")
            print("C) Search by Book Title")
            print("D) Return to the search menu")
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
        """
        A function created to search for a book by ISBN

        Returns:
            True or False based on printList function
        """

        self.printSection("SEARCH BY ISBN")

        isbn = self.getSearchInput("ISBN: ")

        if self.validator.validateISBN(isbn):
            with DatabaseUtils() as db:
                return self.printList(
                    "search results", "all search results",
                    BOOK_HEADERS, db.getBookByISBN(isbn))

    def searchBookByTitle(self):
        """A function created to search for a book by Title

        Returns:
            True or False based on printList function
        """

        self.printSection("SEARCH BY TITLE")

        title = self.getSearchInput("Title: ")

        if self.validator.validateTitle(title):
            with DatabaseUtils() as db:
                return self.printList(
                    "search results", "all search results",
                    BOOK_HEADERS, db.getBooksByTitle(title))

    def searchBookByAuthor(self):
        """A function created to search for a book by Author

        Returns:
            True or False based on printList function
        """

        self.printSection("SEARCH BY AUTHOR")
        author = self.getSearchInput("Author: ")

        if self.validator.validateAuthor(author):
            with DatabaseUtils() as db:
                return self.printList(
                    "search results", "all search results",
                    BOOK_HEADERS, db.getBooksByAuthor(author))

    def wantsToBorrow(self):
        """A function to check if the user wants to borrow a searched book"""

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
                    currentdate = datetime.now()
                    dueDate = currentdate.date() + timedelta(days=7)

                    eventID = self.calendar.createCalendarEvent(
                        isbn, self.username)

                    with DatabaseUtils() as db:

                        if(db.insertBorrow(isbn, self.username, eventID)):
                            print(
                                "Book ISBN {} sucessfully borrowed by {}."
                                .format(isbn, self.username))
                            print(
                                "Due date is: " + dueDate.strftime(
                                    DATE_FORMAT))
                            print("A event has been set in our GoogleCalendar")
                        else:
                            self.calendar.removeCalendarEvent(
                                isbn, self.username)
                            print("Book unsucessfully borrowed due")

    def borrowBook(self):
        """A function created to borrow a book

        Returns:
            False
        """

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
                    eventID = None

                    with DatabaseUtils() as db:
                        eventID = db.updateReturnDate(isbn, self.username)

                    if eventID is not None:
                        print(
                            "Book ISBN {} sucessfully returned by {}."
                            .format(isbn, self.username))
                        self.calendar.removeCalendarEvent(isbn, self.username)
                        print(
                            "EventID {} successfully remove"
                            .format(eventID))
                    else:
                        print(
                            "Book unsucessfully returned by {} due to db error"
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
                self.returnBookQR()
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

            isbn = self.QR.readQR()
            self.returnBook(isbn)
            runAgain = self.repeatsFunction("return")

    def repeatsFunction(self, action):
        """
        A function created to ask the user if they wish to repeat the action

        Args:
            action: borrow or return - action to be repeated if required

        Returns:
            True if they would like to borrow/return again
            False if not
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
