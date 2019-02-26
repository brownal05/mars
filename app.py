import pandas as pd
from flask import Flask, jsonify, render_template, request, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    input_data = mongo.db.mars.find_one()

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", input_data=input_data)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()

    mongo.db.mars.update({}, mars_data,  upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
