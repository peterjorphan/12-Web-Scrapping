## Step 2 - MongoDB and Flask Application
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

# - Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
from flask import Flask, jsonify, render_template, redirect
app = Flask(__name__)

import pymongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

@app.route("/scrape")
def scrape():
    from scrape_mars import scrape
    # - Store the return value in Mongo as a Python dictionary.
    db = client.mars_db
    db.mars.drop()
    db.mars.insert_one(scrape())
    return redirect("/")

# - Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
@app.route('/')
def index():
    db = client.mars_db
    data_dict = db.mars.find_one()
    return render_template("index.html", dict=data_dict)

if __name__ == '__main__':
    app.run(debug=True)
