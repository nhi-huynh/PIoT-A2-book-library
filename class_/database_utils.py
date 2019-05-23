import MySQLdb


class DatabaseUtils:
    """
    A class used to represent different utilites of the database

    Attributes
    ----------
    connection : string
        the _____
    HOST : string
        the host ip address
    USER : string
        the username to login
    PASSWORD : string
        the password to login
    DATABASE : string
        the database name

    Methods
    -------
    close():
    __enter__():
    __exit__(type, value, traceback):
    createBookTable():
        A function created to create the book database
        if it doesnt already exist
    createBorrowTable():
        A function created to create the borrow database
        if it doesnt already exist
    insertSampleBook():
        A function created to insert a sample book to the book database
    getEventID(isbn, username):
        A function created to get the event id from a specific row
    getBooksByISBN(isbn):
        A function created to get all the books that match the isbn
    getBooksByTitle(title):
        A function created to get all the books that match the title
    getBooksByAuthor(author):
        A function created to get all the books that match the author
    getBooks():
        A function created to return all entries in the Book table
    getBorrows():
        A function created to return all entries in the Borrow table
    stillOnLoan(username, isbn):
        A function created to get the borrow date and return date of
        a book the user has borrowed
    getBorrowsByUsername(username):
        A function created to get all the books the user has borrowed
    insertBook(title, author, yearPublished):
        A function created to insert a book into the book table
    insertBorrow(isbn, username):
        A function created to insert a book into the borrow table
    updateReturnDate(isbn, username):
        A function created to update the return date value
    """

    HOST = "35.189.60.60"
    USER = "root"
    PASSWORD = "piot"
    DATABASE = "Library"       # Database name

    def __init__(self, connection=None):
        if(connection is None):
            connection = MySQLdb.connect(
                DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createBookTable(self):
        """A function created to create the book database
        if it doesnt already exist"""

        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Book (
                    ISBN int not null auto_increment,
                    Title text not null,
                    Author text not null,
                    YearPublished int not null,
                    constraint PK_Book primary key (ISBN))
                """)
            self.connection.commit()

    def createBorrowTable(self):
        """A function created to create the borrow database
        if it doesnt already exist"""

        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Borrow (
                    borrowID int not null auto_increment,
                    ISBN int not null,
                    username VARCHAR(50) not null,
                    borrowDate DATETIME not null,
                    dueDate DATE not null,
                    returnDate DATETIME DEFAULT null,
                    eventID VARCHAR(50) DEFAULT null,
                    constraint PK_Borrow primary key (borrowID),
                    constraint FK_Borrow_Book foreign key (ISBN)""" + """ references Book (ISBN))
                """)
            self.connection.commit()

    def insertSampleBook(self):
        """A function created to insert a sample book to the book database"""

        with self.connection.cursor() as cursor:
            isEmpty = cursor.execute("""
                select isbn from Book
                """)

            # print("Book table has {} rows".format(isEmpty))
            if isEmpty == 0:
                self.insertBook("Frankenstein", "Mary Shelley", "1818")
                self.insertBook("Doraemon", "Fujiko Fujio", "1969")
                self.insertBook("Dragon Ball", "Akira Toriyama", "1984")
                self.insertBook("Naruto", "Masashi Kishimoto", "1997")
                self.insertBook("One Piece", "Eiichiro Oda", "1997")
                self.connection.commit()

    # def getEventID(self, isbn, username):
    #     """
    #     A function created to get the event id from a specific row

    #     Args:
    #         isbn: string to find in table
    #         username: string to find in table

    #     Returns:
    #         the eventid that matches the row that the username and isbn match
    #     """

    #     with self.connection.cursor() as cursor:
    #         cursor.execute(
    #             """select eventID from Borrow where username = %s
    #             and ISBN = %s""", (username, isbn,))
    #         return cursor.fetchone()

    def getBookByISBN(self, isbn):
        """
        A function created to get all the books that match the isbn

        Args:
            isbn: string to find in table

        Returns:
            all books that match
        """

        with self.connection.cursor() as cursor:
            cursor.execute("""select ISBN, Title, Author, YearPublished from Book
            where ISBN = %s""", (isbn,))
            return cursor.fetchall()

    def getBooksByTitle(self, title):
        """
        A function created to get all the books that match the title

        Args:
            title: string to find in table

        Returns:
            all books that match
        """

        with self.connection.cursor() as cursor:
            cursor.execute("""select ISBN, Title, Author, YearPublished from Book
            where Title like %s""", ("%" + title + "%",))
            return cursor.fetchall()

    def getBooksByAuthor(self, author):
        """
        A function created to get all the books that match the author

        Args:
            author: string to find in table

        Returns:
            all books that match
        """

        with self.connection.cursor() as cursor:
            cursor.execute("""select ISBN, Title, Author, YearPublished from Book
            where Author like %s""", ("%" + author + "%",))
            return cursor.fetchall()

    def getBooks(self):
        """A function created to return all entries in the Book table"""

        with self.connection.cursor() as cursor:
            cursor.execute("""select ISBN, Title, Author,
            YearPublished from Book""")
            return cursor.fetchall()

    def getBorrows(self):
        """A function created to return all entries in the Borrow table"""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """select borrowID, ISBN, username, borrowDate, dueDate,
                returnDate from Borrow""")
            return cursor.fetchall()

    def stillOnLoan(self, username, isbn):
        """
        A function created to get the borrow date and return date of a
        book the user has borrowed

        Args:
            isbn: string to find in table
            username: string to find in table

        Returns:
            borrowDate and returnDate
        """

        with self.connection.cursor() as cursor:
            cursor.execute("""select borrowDate, dueDate from Borrow
                where username = %s and ISBN = %s and
                returnDate IS NULL LIMIT 1""", (username, isbn,))
            return cursor.fetchone()

    def getBorrowsByUsername(self, username):
        """
        A function created to get all the books the user has borrowed

        Args:
            username: string to find in table

        Returns:
            all books that match
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                """select borrowID, ISBN, username, borrowDate, dueDate,
                returnDate, eventID from Borrow where username = %s""", (
                    username,))
            return cursor.fetchall()

    def insertBook(self, title, author, yearPublished):
        """
        A function created to insert a book into the book table

        Args:
            isbn: string to find in table
            username: string to find in table

        Returns:
            True if exactly one row in the table is added or modified
            False if otherwise
        """

        with self.connection.cursor() as cursor:
            cursor.execute("""
            insert into Book (Title, Author, YearPublished)
            values (%s, %s, %s)""", (title, author, yearPublished))
        self.connection.commit()

        return cursor.rowcount == 1

    def insertBorrow(self, isbn, username, eventID):
        """
        A function created to insert a book into the borrow table

        Args:
            isbn: string that is the ISBN of the book
            username: the username of the person who borrowed the book

        Returns:
            True if exactly one row in the table is added or modified
            False if otherwise
        """

        with self.connection.cursor() as cursor:
            cursor.execute("""
            insert into Borrow (ISBN, username, borrowDate, dueDate, eventID)
            values (%s, %s, NOW(), DATE_ADD(NOW(),
            INTERVAL 7 DAY), %s)""", (isbn, username, eventID))
        self.connection.commit()

        return cursor.rowcount == 1

    def updateReturnDate(self, isbn, username):  # returnDate
        """
        A function created to update the return date value and
        return the eventID for that borrow

        Args:
            isbn: string that is the ISBN of the book
            username: the username of the person who borrowed the book

        Returns:
            the eventid that matches the row that the username and isbn match
        """

        eventID = None

        with self.connection.cursor() as cursor:
            cursor.execute(
                """select eventID
                from Borrow
                where username = %s
                and ISBN = %s
                AND returnDate IS NULL""",
                (username, isbn,))
            eventID = cursor.fetchone()

        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE Borrow
                SET returnDate = NOW()
                WHERE ISBN = %s AND username = %s AND returnDate IS NULL""",
                (isbn, username,))

        self.connection.commit()

        return eventID
        # return cursor.rowcount == 1
