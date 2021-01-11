# Import tools

## Use Flask to render a template.
from flask import Flask, render_template
## use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
## use the scraping code, we will convert from Jupyter notebook to Python.
import scraping


# Create a Flask instance called app 
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
# This function is what links our visual representation of our work, our web app, to the code that powers it.

## tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
## URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
## Define the root route and what would be displayed on the homepage 
@app.route("/")
def index():
    ## uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. We will also assign that path to the mars variable for use later.
    mars = mongo.db.mars.find_one()
    ## return render_template("index.html" tells Flask to return an HTML template using an index.html file.
    ## ,mars=mars) tells Python to use the "mars" collection in MongoDB.
    return render_template("index.html", mars=mars)


# Set up our scraping route. 
# This route will be the "button" of the web application, the one that will scrape updated data when we tell it to from the homepage of our web app. It'll be tied to a button that will run the code when it's clicked.

## Definethe “/scrape” route
@app.route("/scrape")
def scrape():
   ## assign a new variable that points to our Mongo database 
   mars = mongo.db.mars
   ## create a new variable to hold the newly scraped data. Reference the scrape_all function in the scraping.py file exported from Jupyter Notebook.
   mars_data = scraping.scrape_all()
   ## We're inserting data, so first we'll need to add an empty JSON object with {}.
   ## Next, we'll use the data we have stored in mars_data
   ## upsert=True indicates to Mongo to create a new document if one doesn't already exist
   mars.update({}, mars_data, upsert=True)
   ## Add a message to indicate successful scraping
   return "Scraping Successful!"

# Run the code if we are running it directly from app.py
if __name__ == "__main__":
    app.run()