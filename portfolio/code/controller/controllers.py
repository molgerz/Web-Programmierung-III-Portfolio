# TODO
from cryptography.fernet import Fernet
from portfolio.config import key, db
from portfolio.model.models import User, Book, UserHasBook
import logging

logging.basicConfig(
    filename="../logging.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s %(message)s"
)

class Usercontroller:

    def __init__(self):
        self.dbc = Databasecontroller()

    def login(self, email, pw):
        """
        Loggs a user in with given email and passwort
        :param email: Emailaddress of the user
        :param pw: Password of the user
        :return: User object if users exists in DB, None otherwise
        """
        # TODO
        return self.dbc.find_user_by_credentials(email, pw)

    def create_user(self, firstname, lastname, email, password):
        """
        Creates a new User in Database.
        :param firstname:
        :param lastname:
        :param email:
        :param password:
        :return: Returns True if creation has been successfully. False otherwise
        """
        f = Fernet(key)
        # convert password to bytes
        password = bytes(password, "utf-8")
        password = f.encrypt(password)
        password = password.decode("utf-8")
        # TODO
        # add user to database
        user = User(firstname=firstname, lastname=lastname, email=email, password=password)
        self.dbc.create_user(user)

        # check if creation was successful
        if self.dbc.find_user_by_credentials(email, f.decrypt(password).decode('utf-8')) is None:
            return False
        else:
            return True


class Databasecontroller:

    def find_user_by_credentials(self, email, pw):
        """
        Searches a User by the credentials in DB
        :param email:
        :param pw:
        :return: User object if the user can be found, None otherwise
        """
        f = Fernet(key)
        # TODO
        try:
            users = User.query.filter_by(email=email).all()
            for user in users:
                decrypted_pw = f.decrypt(user.password).decode('utf-8')
                if pw == decrypted_pw:
                    logging.info(f"User '{email}' was successfully queried in the database")
                    return user
            raise ValueError
        # TODO
        except ConnectionError:
            logging.error("Connection to the database books.db could not be established")
            return None
        except ValueError:
            logging.warning(f"The combination of the credentials with the email '{email}' "
                            f"could not be found in the database")
            return None

    def add_reservation(self, reservation):
        """
        Adds a reservation for a book in the DB
        :param reservation:
        """
        # TODO
        try:
            db.session.add(reservation)
            db.session.commit()
            logging.info(f"The book with the bookid '{reservation.bookid}' "
                         f"was successfully reserved by the user with the userid '{reservation.userid}'")
        except ConnectionError:
            logging.error("Connection to the database books.db could not be established")

    def create_user(self, user):
        """
        Creates a user in Database
        :param user:
        """
        # TODO
        try:
            db.session.add(user)
            db.session.commit()
            logging.info(f"The user '{user.email}' was successfully added to the database")
        except ConnectionError:
            logging.error("Connection to the database books.db could not be established")

    def get_all_books(self):
        """
        Gets a list of all book in the Database
        :return: List of Books
        """
        # TODO
        try:
            list_of_books = Book.query.all()
            if list_of_books is None:
                logging.info("A list of books was successfully requested from the database, but the list is empty")
            else:
                logging.info("A list of books was successfully requested from the database")
            return list_of_books
        except ConnectionError:
            logging.error("Connection to the database books.db could not be established")

    def change_reservestatus(self, bookid, status):
        """
        Sets the revervation of a book
        :param bookid: The id of the book
        :param status: The status the book with the given ID should have
        """
        # TODO
        try:
            Book.query.filter_by(id=bookid).update({"status": status})
            db.session.commit()
            logging.info(f"The status of the book with the bookid '{bookid}' was successfully changed in '{status}'")
        except ConnectionError:
            logging.error("Connection to the database books.db could not be established")

    def get_reserved_books_for_user(self, userid):
        """
        Fetches all books from the Database a user has reserved
        :param userid:
        :return: A list of books
        """
        # TODO
        try:
            reserved_books_for_user = UserHasBook.query.filter_by(userid=userid).all()
            if reserved_books_for_user is None:
                logging.info(f"A list of books for the user with the userid '{userid}' "
                         f"was successfully requested from the database, but the list is empty")
            else:
                logging.info(f"A list of books for the user with the userid '{userid}' "
                         f"was successfully requested from the database")
            return reserved_books_for_user
        except ConnectionError:
            logging.error("Connection to the database books.db could not be established")

    def get_book_by_id(self, bookid):
        """
        Finds a book by its ID
        :param bookid:
        :return: A book object if the id can be found, None otherwise
        """
        # TODO
        try:
            requested_book = Book.query.get(bookid)
            if requested_book is None:
                raise ValueError
            else:
                logging.info(f"The book with bookid '{bookid}' was successfully queried in the database")
                return requested_book
        except ConnectionError:
            logging.error("Connection to the database books.db could not be established")
            return None
        except ValueError:
            logging.error(f"The book with the bookid '{bookid}' does not exist")
            return None


class Bookcontroller:
    def __init__(self):
        self.dbc = Databasecontroller()

    def get_all_books(self):
        """
        Returns all books
        :return: a list of books or None
        """
        # TODO
        return self.dbc.get_all_books()

    def reserve_book(self, userid, bookid):
        """
        Reserves a book with the given id for the given user id
        :param userid:
        :param bookid:
        """
        # Hint: check if book isn't already reserved (e.g. page reload)
        # TODO
        book = self.dbc.get_book_by_id(bookid)
        if book is not None:
            if book.status == "verfügbar":
                reservation = UserHasBook(bookid=bookid, userid=userid)
                new_status = "reserviert"
                self.dbc.change_reservestatus(bookid, new_status)
                self.dbc.add_reservation(reservation)

    def get_all_books_for_user(self, user_id):
        """
        Returns all books reserved by a user
        :param user_id:
        :return:
        """
        # TODO
        list_of_all_books_for_user = []
        reservation_with_userid = self.dbc.get_reserved_books_for_user(user_id)
        for reservation in reservation_with_userid:
            list_of_all_books_for_user.append(self.dbc.get_book_by_id(reservation.bookid))
        return list_of_all_books_for_user
