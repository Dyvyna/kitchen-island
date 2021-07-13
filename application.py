import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from py_edamam import PyEdamam

app_key = os.environ['KEY']

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

e = PyEdamam(recipes_appid='df633bb0',
           recipes_appkey=app_key)

health = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/list", methods=["GET"])
def list():
    health =""
    ingredients = request.args.get("search")
    if request.args.get("choice1"):
        health +="&diet=balanced"
    if request.args.get("choice2"):
        health +="&diet=low-carb"
    if request.args.get("choice3"):
        health += "&health=vegetarian"
    if request.args.get("choice4"):
        health += "&health=vegan"
    if request.args.get("choice5"):
        health += "&health=sugar-conscious"
    if request.args.get("choice6"):
        health += "&health=low-fat"


    print(f"HEALTH: {ingredients}{health} ")

    recipes_list = e.search_recipe(ingredients+health+"&to=5")

    if not recipes_list:
        return apology(e.name, e.code)
    else:
        for recipe in recipes_list:
            print(f"recipe, {recipe}")
            print(f"recipe, {recipe.image}")
            break
        return render_template("list.html", recipes_list = recipes_list)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)