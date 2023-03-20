from portfolio.config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False)


class UserHasBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bookid = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
