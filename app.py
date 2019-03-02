from flask import Flask, render_template, jsonify, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Use PyMongo to establish Mongo Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #get one record to populate the home page
    mars_data = mongo.db.mars_data.find_one()
    return render_template(("index.html"), mars_data = mars_data)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    scrape_data = scrape_mars.scrape()
    mars_data.update({}, scrape_data, upsert=True)
    #return jsonify(scrape_data)
    
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

