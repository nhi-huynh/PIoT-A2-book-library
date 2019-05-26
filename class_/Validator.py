from class_.DatabaseUtils import DatabaseUtils


class Validator:
    """A class used to represent the validation of input"""

    def __init__(self):
        pass

    def validateISBN(self, isbn):
        """
        A function to validate the ISBN entered

        Args:
            isbn: string to be validated

        Returns:
            True if the input is of valid length and are all digits
            False if not, or is none
        """
        if isbn is None:
            return False

        if (len(isbn) < 10 or len(isbn) > 13) or not isbn.isdigit():
            print("Invalid ISBN")
            print("ISBN's were 10 digits until December 2006, they now consist of 13 digits,\
            \n you must enter atleast 10 digits and no more than 13.\
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
            True if the input is of valid length and valid input
            False if not, or is none
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
            True if the input is of valid length and valid input
            False if not, or is none
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
            True is the isbn exists
            False if it doesnt exist
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
            True is the book is on loan to this user
            False if it isnt
        """

        # check if the user has not returned the book
        with DatabaseUtils() as db:
            currentLoan = db.stillOnLoan(username, isbn)
            if currentLoan is not None:
                print("You are currently borrowing book ISBN {}".format(isbn))
                print("Book ISBN {} was borrowed on {}".format(
                    isbn, currentLoan[0]))
                print("It will be due on {}".format(currentLoan[1]))
                return True
            else:
                return False
