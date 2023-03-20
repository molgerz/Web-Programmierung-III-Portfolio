# TODO
from portfolio.controller.controllers import Usercontroller, Bookcontroller
from flask import Flask, render_template, request, session, redirect
from portfolio.config import dbname, db

# create the app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = dbname
db.init_app(app)
app.secret_key = "lkjkljasdfklaskjf"
# TODO
uc = Usercontroller()
bc = Bookcontroller()


@app.route("/")
def show_homepage():
    """
    Shows the start page
    :return:
    """
    session.clear()
    return render_template("homepage.html")


@app.route("/login", methods=['POST'])
def login():
    """Used when the user filled out the login form and redirects the user to home.html
    in case, that the user has been successfully logged in. Otherwise, he is redirected to the homepage.html"""
    session.clear()
    # TODO
    # get credentials from userinput
    email = request.form.get("email")
    password = request.form.get("password")
    # check credentials
    user = uc.login(email=email, pw=password)
    # redirect user
    if user is not None:
        session["user"] = {"id": user.id, "firstname": user.firstname, "lastname": user.lastname, "email": user.email}
        user = session["user"]
        list_of_all_books_for_user = bc.get_all_books_for_user(user["id"])
        list_of_all_books = bc.get_all_books()
        return render_template("home.html",
                               list_of_all_books=list_of_all_books,
                               user=user,
                               list_of_all_books_for_user=list_of_all_books_for_user)
    else:
        return render_template("homepage.html")


@app.route("/logoutuser")
def logoutUser():
    session.clear()
    return render_template("homepage.html")


@app.route("/createUser", methods=['POST'])
def create_user():
    """Used, after the user has filled out the registration form and submits.
    User is now created and the user is redirected to the homepage.html"""
    # TODO
    # get credentials
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")
    # create account
    new_user = uc.create_user(firstname=firstname, lastname=lastname, email=email, password=password)
    # redirect to homepage if creation succeed
    if new_user:
        return render_template("homepage.html")


@app.route("/borrowbook", methods=['POST'])
def borrow_book():
    """Used, when the user clicks reserve in the frontend. Afterwards, the user is redirected to /showhome"""
    # TODO
    user = session["user"]
    bookid = request.form.get("bookid")
    bc.reserve_book(user["id"], bookid)
    return redirect("/showhome")


@app.route("/showhome")
def showHome():
    """Shows the book overview (home.html) with available and reserved books"""
    # TODO
    user = session["user"]
    list_of_all_books_for_user = bc.get_all_books_for_user(user["id"])
    list_of_all_books = bc.get_all_books()
    return render_template("home.html",
                           list_of_all_books=list_of_all_books,
                           user=user,
                           list_of_all_books_for_user=list_of_all_books_for_user)


@app.route("/showCreateUser")
def show_create_user():
    """Opens the createuser.html"""
    # TODO
    session.clear()
    return render_template("createuser.html")


@app.route("/logout")
def logout():
    # THIS FUNCTION IS OBSOLETE. YOU DON'T HAVE TO USE THIS IN YOUR PORTFOLIO
    session.clear()


with app.app_context():
    db.create_all()
app.run(debug=True)
