import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mystery.db")

# Ensure reponses aren't cached
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/")
@login_required
def index():
    """Introduction to Mystery and Instructions"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("instructions.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login User"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("ERROR: No Username Entered - Must provide username!", "error")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("ERROR: No Password Entered - Must provide password!", "error")
            return render_template("login.html")

         # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["passwordhash"], request.form.get("password")):
            flash("ERROR: Username or Password is Incorrect", "error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout User"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmpassword")

        # Alert user if email is missing
        if not email:
            flash("ERROR: Missing Email - Ensure all fields are correctly filled in before registering!", "error")
            return render_template("register.html")

        # Alert user if username is missing
        if not username:
            flash("ERROR: Missing Username - Ensure all fields are correctly filled in before registering!", "error")
            return render_template("register.html")

        # Alert user if password is missing
        if not password:
            flash("ERROR: Missing Password - Ensure all fields are correctly filled in before registering!", "error")
            return render_template("register.html")

        # Alert user if the password confirmation does not match the original password
        if password != confirmPassword:
            flash("ERROR: Passwords Do Not Match!", "error")
            return render_template("register.html")


        # Generate password hash for user
        passwordHash = generate_password_hash(password)

        # Try to store information into the users table; however, render an alert if the username already exists and cancel registration
        # Note that db.execute(INSERT...) will fail if the username entered already exists in the database since it was defined as a UNIQUE INDEX
        try:
            db.execute("INSERT INTO users (email, username, passwordhash) VALUES (?, ?, ?)", email, username, passwordHash)
        except:
            flash("ERROR: Username Already Exists - Register again with a new username!", "error")
            return render_template("register.html")

        # Let the user know that they have registered successfully and load the login page
        flash("Success: You are Now Registered!", "success")

        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/map")
@login_required
def map():
    """Access the Map to Display Unlocked Locations"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    # Get the locations that the user has unlocked
    locations = db.execute("SELECT unlocked FROM locations WHERE user_id = ?", session["user_id"])

    # Locations will not exist if the user has not discovered any new places. locations[0]["unlocked"] DOES NOT work if locations does not exist
    if not locations:
        return render_template("map.html", username=username)
    else:
        locations = locations[0]["unlocked"]
        return render_template("map.html", username=username, placesDiscovered=locations)


@app.route("/notebook", methods=["GET", "POST"])
@login_required
def notebook():
    """Opens or Saves the User's Notes"""

    if request.method == "POST":
        # Save the users notebook when they click "Save Notes"
        notes = request.form.get("notes")
        db.execute("UPDATE users SET notes = ? WHERE user_id = ?", notes, session["user_id"])

        # Get the username from the users table in the mystery database
        username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

        return render_template("notebook.html", username=username, notes=notes)

    else:
        # Get the user's previously saved notes
        notes = db.execute("SELECT notes FROM users WHERE user_id = ?", session["user_id"])[0]["notes"]

        # Get the username from the users table in the mystery database
        username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

        return render_template("notebook.html", username=username, notes=notes)



@app.route("/policestation")
@login_required
def policstation():
    """Takes User to the Police Station"""

    # Get the locations that the user has unlocked
    locations = db.execute("SELECT unlocked FROM locations WHERE user_id = ?", session["user_id"])

    # If locations does not yet exist, this is the user's first time going to the station and has not discovered any places.
    if not locations:
        db.execute("INSERT INTO locations (user_id, unlocked) VALUES(?, ?)", session["user_id"], 0)

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    # Get the locations again that the user has unlocked (second locations get required)
    locations = db.execute("SELECT unlocked FROM locations WHERE user_id = ?", session["user_id"])[0]["unlocked"]

    # If locations does not equal 4, user has not yet foudn the proffesor, show locked computer
    if locations is not 4:
        print()
        return render_template("policestationlocked.html", username=username)

    #Else, the user discovered the professor and is allowed to input who did it
    else:
        return render_template("policestationunlocked.html", username=username)


@app.route("/prosecute", methods=["GET", "POST"])
@login_required
def prosecute():
    """User Enters Criminal's Name"""

    if request.method == "POST":
        accused = request.form.get("suspect")

        # Get the username from the users table in the mystery database
        username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

        if accused == "Edwin Thorby":
            return render_template("promoted.html", username=username)

        else:
            # Forget user if he prosecutes the incorrect suspect
            db.execute("DELETE FROM users WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM locations WHERE user_id = ?", session["user_id"])
            session.clear()
            return render_template("terminated.html", username=username)


@app.route("/office")
@login_required
def office():
    """Takes User to the Office"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("office.html", username=username)


@app.route("/letter")
@login_required
def letter():
    """Zoom In on the Letter on the Desk"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officeletter.html", username=username)


@app.route("/smalldrawer")
@login_required
def smalldrawer():
    """Open Small Drawer"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officesmalldrawer.html", username=username)


@app.route("/synergyaddressnote")
@login_required
def synergyaddressnote():
    """Show the Sticky Note with Synergy's Address"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    # Get the locations that the user has unlocked
    locations = db.execute("SELECT unlocked FROM locations WHERE user_id = ?", session["user_id"])

    # If locations does not yet exist, this is the users first time discovering Synergy. Insert location discovered
    if not locations:
        db.execute("INSERT INTO locations (user_id, unlocked) VALUES(?, ?)", session["user_id"], 2)

    if locations != 2:
        db.execute("UPDATE locations SET unlocked = 2 WHERE user_id = ?", session["user_id"])

    return render_template("officesynergyaddressnote.html", username=username)


@app.route("/codebooks")
@login_required
def codebooks():
    """Show User the Books on the Shelf that Contain the Ciphered Code"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officecodebooks.html", username=username)


@app.route("/book1")
@login_required
def book1():
    """Show User What's inside the 1st Book in the Code Sequence"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officebook1.html", username=username)


@app.route("/book2")
@login_required
def book2():
    """Show User What's inside the 2nd Book in the Code Sequence"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officebook2.html", username=username)


@app.route("/book3")
@login_required
def book3():
    """Show User What's inside the 3rd and Last Book in the Code Sequence"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officebook3.html", username=username)


@app.route("/book4")
@login_required
def book4():
    """Show User What's inside the 4th Book (Decoy from Code Sequence)"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officebook4.html", username=username)


@app.route("/book5")
@login_required
def book5():
    """Show User What's inside the 5th Book (Decoy from Code Sequence)"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officebook5.html", username=username)


@app.route("/book6")
@login_required
def book6():
    """Show User What's inside the 6th Book (Decoy from Code Sequence)"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officebook6.html", username=username)


@app.route("/deskclock")
@login_required
def deskclock():
    """Show Time on Desk Clock"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officedeskclock.html", username=username)


@app.route("/coffeechest")
@login_required
def coffeechest():
    """Open Chest on Coffee Table"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officecoffeechest.html", username=username)


@app.route("/cipher")
@login_required
def cipher():
    """Show Cipher Key"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officecipher.html", username=username)


@app.route("/couplepic")
@login_required
def couplepic():
    """Show Lucia and Edwin Picture"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("officecouplepic.html", username=username)




@app.route("/lab")
@login_required
def lab():
    """Take User to the Laboratory at Synergy"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("lab.html", username=username)


@app.route("/computer", methods=["GET", "POST"])
@login_required
def computer():
    """Opens Login Screen & Home Screen of Lab Computer"""

    if request.method == "POST":
        codeEntered = request.form.get("code")

        # Get the username from the users table in the mystery database
        username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

        if codeEntered == "D3@th is life$ mercy":
            return render_template("labcomputerhome.html", username=username)
        else:
            return render_template("labcomputerfaillogin.html", username=username)

    else:
        # Get the username from the users table in the mystery database
        username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

        return render_template("labcomputerlogin.html", username=username)


@app.route("/computerhome", methods=["GET", "POST"])
@login_required
def computerhome():
    """Returns User from Folder or File to the Home Screen"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerhome.html", username=username)


@app.route("/privfolder")
@login_required
def privfolder():
    """Open the Priv Folder on the Professor's Computer"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerprivfolder.html", username=username)


@app.route("/apologyletter")
@login_required
def apologyletter():
    """Open the Apology Letter from Priv Folder"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerprivfolderapology.html", username=username)


@app.route("/note")
@login_required
def note():
    """Open Trust No One Note from Priv Folder"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerprivfoldernote.html", username=username)


@app.route("/earlytrialfolder")
@login_required
def earlytrialfolder():
    """Open Early Trial Folder"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerearlytrialfolder.html", username=username)


@app.route("/newmexicoaccident")
@login_required
def newmexicoaccident():
    """Open New Mexico Accident Video"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerearlytrialfolderaccident.html", username=username)


@app.route("/nexusdrawing")
@login_required
def nexusdrawing():
    """Open Nexus Drawing"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerearlytrialfoldernexus.html", username=username)


@app.route("/familyfolder")
@login_required
def familyfolder():
    """Open Folder with Family Pictures"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerfamilyfolder.html", username=username)


@app.route("/beatriceportrait")
@login_required
def beatriceportrait():
    """Open Portrait of Beatrice"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerfamilyfolderbeatrice.html", username=username)


@app.route("/cabinphoto")
@login_required
def cabinphoto():
    """Open Photo of Cabin"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("labcomputerfamilyfoldercabin.html", username=username)


@app.route("/cabinplate")
@login_required
def cabinplate():
    """Zoom in on Cabin Plate"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    # Get the locations that the user has unlocked
    locations = db.execute("SELECT unlocked FROM locations WHERE user_id = ?", session["user_id"])

    # If locations does not equal 3, this is the users first time discovering the Cabin. Insert location discovered
    if locations is not 3:
        db.execute("UPDATE locations SET unlocked = 3 WHERE user_id = ?", session["user_id"])

    return render_template("labcomputerfamilyfoldercabinplate.html", username=username)


@app.route("/cabin")
@login_required
def cabin():
    """Go to Cabin"""

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("cabin.html", username=username)


@app.route("/professor")
@login_required
def professor():
    """Approach the Dying Professor"""

    # Get the locations that the user has unlocked
    locations = db.execute("SELECT unlocked FROM locations WHERE user_id = ?", session["user_id"])

    # If locations does not equal 4, this is the users first time talking to the proffesor. Insert final location
    if locations is not 4:
        db.execute("UPDATE locations SET unlocked = 4 WHERE user_id = ?", session["user_id"])

    # Get the username from the users table in the mystery database
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])[0]["username"]

    return render_template("cabinprofessor.html", username=username)






