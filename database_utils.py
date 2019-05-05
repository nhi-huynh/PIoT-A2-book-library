import MySQLdb

class DatabaseUtils:
    
    HOST = "35.189.60.60"
    USER = "root"
    PASSWORD = "piot"
    DATABASE = "Library"       #Database name

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
    
    def createBookTable(self):
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
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Borrow (
                    ISBN int not null,
                    username VARCHAR(50) not null,
                    borrowDate date not null,
                    dueDate date not null,
                    returnDate date DEFAULT null,
                    constraint FK_Borrow_Book foreign key (ISBN) references Book (ISBN))
                """)
            self.connection.commit()

    def insertSampleBook(self):
        with self.connection.cursor() as cursor:
            isEmpty = cursor.execute("""
                select isbn from Book
                """) 

            #print("Book table has {} rows".format(isEmpty))
            if isEmpty == 0:
                self.insertBook("Frankenstein", "Mary Shelley", "1818")
                self.insertBook("Doraemon", "Fujiko Fujio", "1969")
                self.insertBook("Dragon Ball", "Akira Toriyama", "1984")
                self.insertBook("Naruto", "Masashi Kishimoto", "1997")
                self.insertBook("One Piece", "Eiichiro Oda", "1997")
                self.connection.commit()

    def getBookByISBN(self, isbn):
        with self.connection.cursor() as cursor:
            cursor.execute("""select ISBN, Title, Author, YearPublished from Book
            where ISBN = %s""", (isbn,))
            return cursor.fetchall()

    def getBooksByTitle(self, title):
        with self.connection.cursor() as cursor:
            cursor.execute("""select ISBN, Title, Author, YearPublished from Book
            where Title like %s""", ("%" + title + "%",))
            return cursor.fetchall()

    def getBooksByAuthor(self, author):
        with self.connection.cursor() as cursor:
            cursor.execute("""select ISBN, Title, Author, YearPublished from Book
            where Author like %s""", ("%" + author + "%",))
            return cursor.fetchall()
        
    def getBooks(self):
        """
        Return all entries in the Book table
        """
        with self.connection.cursor() as cursor:
            cursor.execute("select ISBN, Title, Author, YearPublished from Book")
            return cursor.fetchall()

    def getBorrows(self):
        """
        Return all entries in the Borrow table
        """
        with self.connection.cursor() as cursor:
            cursor.execute("select ISBN, username, borrowDate, dueDate, returnDate from Borrow")
            return cursor.fetchall()

    def stillOnLoan(self, username, isbn):
        """
        Return the borrowDate and returnDate for the username if the book is still on loan.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""select borrowDate, dueDate from Borrow
                where username = %s and ISBN = %s and returnDate IS NULL LIMIT 1""", 
            (username, isbn,))
            return cursor.fetchone() 

    def getBorrowsByUsername(self, username):
        """
        Return all loans record belongs to username
        """
        with self.connection.cursor() as cursor:
            cursor.execute("select ISBN, username, borrowDate, dueDate, returnDate from Borrow where username = %s", (username,))
            return cursor.fetchall()
    
    def insertBook(self, title, author, yearPublished):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            insert into Book (Title, Author, YearPublished) 
            values (%s, %s, %s)""",
            (title, author, yearPublished))
        self.connection.commit()

        return cursor.rowcount == 1

    def insertBorrow(self, isbn, username):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            insert into Borrow (ISBN, username, borrowDate, dueDate) 
            values (%s, %s, CURRENT_DATE(), DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY))""",(isbn, username,))
        self.connection.commit()

        return cursor.rowcount == 1

    def updateReturnDate(self, isbn, username): #, returnDate
        with self.connection.cursor() as cursor:
            cursor.execute("""
            UPDATE Borrow
            SET returnDate = CURRENT_DATE() 
            WHERE ISBN = %s AND username = %s AND returnDate IS NULL
            """,
            (isbn, username,))   #returnDate, 
        self.connection.commit()

        return cursor.rowcount == 1


