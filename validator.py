from database_utils import DatabaseUtils


class Validator:

    def __init__(self):
        pass

    def validateISBN(self, isbn):
        if len(isbn) > 10 or not isbn.isdigit():
            print("Invalid ISBN")
            print("ISBN's were 10 digits until December 2006, they now consist of 13 digits,\
            \n you must enter atleast 10 digits.\
            \nPlease try again\n""")
            return False
        else:
            return True

    def validateTitle(self, title):
        if all(len(title) == 0 or not all(name.isalnum() or name.isspace() for name in title)):
            print("Invalid title.")
            print("Title must contain only letters and/or numbers.")
            print("Please try again.\n")
            return False
        else:
            return True

    def validateAuthor(self, author):
        if all(len(author) == 0 or not all(name.isalpha() or name.isspace() for name in author)):
            print("Invalid author name.")
            print("Name must be letters.")
            print("Please try again.\n")
            return False
        else:
            return True

    def isbnExists(self, isbn):
        # check if isbn exits in the database
        with DatabaseUtils() as db:
            if not db.getBookByISBN(isbn):
                print("Book ISBN {} does not exist".format(isbn))
                print("Please try again")
                return False
            else:
                return True

    def onLoan(self, username, isbn):
        # check if the user has not returned the book
        with DatabaseUtils() as db:
            currentLoan = db.stillOnLoan(username, isbn)
            # print(currentLoan)
            if currentLoan is not None:
                print("You are currently borrowing book ISBN {}".format(isbn))
                print("""Book ISBN {} was borrowed on {} and will be available
                on the {}""".format(isbn, currentLoan[0], currentLoan[1]))
                return True
            else:
                return False
