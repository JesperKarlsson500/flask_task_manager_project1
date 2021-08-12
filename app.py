import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
"""
Since we are not going to push the env.py file to GitHub,
once our app is deployed to Heroku, it won't be able
to find the env.py file, so it will throw an error.
This is why we need to only import env if the os
can find an existing file path for
the env.py file itself.
"""
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    # latest tasks = this
    return render_template("tasks.html", tasks=tasks)
    # This will find all documents from the
    # tasks collection, and assign them to our new 'tasks'


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # This acts as the else statement if
        # no other existing user is found
        # Our variable register will act as
        # a dictionary that will be inserted into the database
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
