from database_utils import DatabaseUtils

class Validator:

    def __init__(self):
        pass

    def validateISBN(self, isbn): 
        if len(isbn) > 13 or not isbn.isdigit():
            print("Invalid ISBN")
            print("ISBN is 13 digits long since December 2006.\
            \nThe old 10-digit ISBN format is no longer supported.\
            \nPlease try again\n""")    
            return False
        else:
            return True

    def validateTitle(self, title): 
        if all(len(name) == 0 or not name.isalnum() for name in title):
            print("Invalid title.")
            print("Title must contain only letters and/or numbers.")
            print("Please try again.\n")  
            return False
        else:
            return True
    
    def validateAuthor(self, author): 
        if all(len(name) == 0 or not name.isalpha() for name in author):
            print("Invalid author name.")
            print("Name must be letters.")
            print("Please try again.\n")
            return False
        else:
            return True

    def isbnExists(self, isbn):
        #check if isbn exits in the database
        with DatabaseUtils() as db:
            if not db.getBookByISBN(isbn):
                print("Book ISBN {} does not exist in the database".format(isbn))
                print("Please try again")
                return False
            else:
                return True
    
    def onLoan(self, username, isbn):       
        #check if the user has not returned the book 
        with DatabaseUtils() as db:
            currentLoan = db.stillOnLoan(username, isbn)
            #print(currentLoan)
            if currentLoan != None:
                print("You are currently borrowing book ISBN {}".format(isbn))
                print("Book ISBN {} was borrowed on {} and will be due on {}".format(isbn, currentLoan[0], currentLoan[1]))
                return True
            else:
                return False

    
        