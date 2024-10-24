import requests
import json
from flask import Flask, render_template, request, url_for, redirect, flash, abort, session
from datetime import datetime
import sqlite3
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "lngfelorjhfoewqjf"

UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

global order
order = []


# Database initialisation
def init_db():
    with sqlite3.connect(r"C:\Users\738290\Downloads\SQLiteDatabaseBrowserPortable\CafeMenuDB.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name text NOT NULL,
            item_price real NOT NULL,
            item_type text NOT NULL,
            item_image text NOT NULL
        )""")
        conn.commit()


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/menu")
def menu_page():
    with sqlite3.connect(r"C:\Users\738290\Downloads\SQLiteDatabaseBrowserPortable\CafeMenuDB.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        items = cursor.fetchall()
        return render_template("menu.html", items=items)


@app.route("/add", methods=["GET", "POST"])
def add_page():
    if request.method == "POST":
        item_name = request.form.get("item_name")
        item_price = request.form.get("item_price")
        item_type = request.form.get("item_type")
        item_file = request.files["item_file"]

        path = os.path.join(app.config["UPLOAD_FOLDER"], item_file.filename)
        item_file.save(path)

        with sqlite3.connect(r"C:\Users\738290\Downloads\SQLiteDatabaseBrowserPortable\CafeMenuDB.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO menu (item_name, item_price, item_type, item_image)
            VALUES (?,?,?,?)""", (item_name, item_price, item_type, path))
            conn.commit()

        print(item_name, item_type, item_price)
        return redirect("/menu")
    return render_template("add.html")


@app.route("/add_to_cart/<food_type>/<food_id>", methods=["GET", "POST"])
def app_to_cart_page(food_type, food_id):
    global order
    order.append(food_id)
    with sqlite3.connect(r"C:\Users\738290\Downloads\SQLiteDatabaseBrowserPortable\CafeMenuDB.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT item_price FROM menu WHERE item_id == {food_id}")
        item_price = cursor.fetchone()
        cursor.execute(f"SELECT item_name FROM menu WHERE item_id == {food_id}")
        item_name = cursor.fetchone()

    flash(f"You have added {item_name} to your Cart for £{item_price}.00")
    return redirect("/menu")

@app.route("/cart")
def cart_page():
    global order
    return render_template("cart.html", order=order)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)