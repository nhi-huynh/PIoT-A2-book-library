from class_.database_utils import DatabaseUtils


class Validator:
    """
    A class used to represent the validation of input

    Methods
    -------
    validateISBN(isbn):
        A function to validate the ISBN entered
    validateTitle(title):
        A function to validate the book title entered
    validateAuthor(author):
        A function to validate the author entered
    isbnExists(isbn):
        A function to check that the isbn exists in the library
    onLoan(username, isbn):
        A function to check if the user has the isbn book on loan
    """

    def __init__(self):
        pass

    def validateISBN(self, isbn):
        """
        A function to validate the ISBN entered

        Args:
            isbn: string to be validated

        Returns:
            True or False
        """
        if isbn is None:
            return False

        if len(isbn) > 10 or not isbn.isdigit():
            print("Invalid ISBN")
            print("ISBN's were 10 digits until December 2006, they now consist of 13 digits,\
            \n you must enter atleast 10 digits.\
            \nPlease try again\n""")
            return False
        else:
            return True

    def validateTitle(self, title):
        """
        A function to validate the book title entered

        Args:
            title: string to be validated

        Returns:
            True or False
        """
        if title is None:
            return False

        if (len(title) == 0 or not all(
                name.isalnum() or name.isspace() for name in title)):
            print("Invalid title.")
            print("Title must contain only letters and/or numbers.")
            print("Please try again.\n")
            return False
        else:
            return True

    def validateAuthor(self, author):
        """
        A function to validate the author entered

        Args:
            author: string to be validated

        Returns:
            True or False
        """
        if author is None:
            return False

        if (len(author) == 0 or not all(
                name.isalpha() or name.isspace() for name in author)):
            print("Invalid author name.")
            print("Name must be letters.")
            print("Please try again.\n")
            return False
        else:
            return True

    def isbnExists(self, isbn):
        """
        A function to check that the isbn exists in the library

        Args:
            isbn: string to be checked

        Returns:
            True or False
        """

        # check if isbn exits in the database
        with DatabaseUtils() as db:
            if not db.getBookByISBN(isbn):
                print("Book ISBN {} does not exist".format(isbn))
                print("Please try again")
                return False
            else:
                return True

    def onLoan(self, username, isbn):
        """
        A function to check if the user has the isbn book on loan

        Args:
            username: string to check records against
            isbn: string to check records against

        Returns:
            True or False
        """

        # check if the user has not returned the book
        with DatabaseUtils() as db:
            currentLoan = db.stillOnLoan(username, isbn)
            # print(currentLoan)
            if currentLoan is not None:
                print("You are currently borrowing book ISBN {}".format(isbn))
                print("Book ISBN {} was borrowed on {}".format(
                    isbn, currentLoan[0]))
                print("It will be due on {}".format(currentLoan[1]))
                return True
            else:
                return False
