#9.5.1

import datetime as dt
import numpy as np
import pandas as pd
#dependencies we need for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

#set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

#The create_engine() function allows us to 
# access and query our SQLite database file.

Base = automap_base()

#Add the following code to reflect the database
Base.prepare(engine, reflect=True)


#With the database reflected, we can save our references to each table.
#Again, they'll be the same references as the ones we wrote earlier in this module. 
#We'll create a variable for each of the classes so that we can reference them later, as shown below.

Measurement = Base.classes.measurement
Station = Base.classes.station


#Finally, create a session link from Python to our database with the following code:
session = Session(engine)

#To define our Flask app, add the following line of code. 
# This will create a Flask application called "app."

app = Flask(__name__)

#Notice the __name__ variable in this code. 
# This is a special type of variable in Python. 
# Its value depends on where and how the code is run. For example, if we wanted to import our app.py 
# file into another Python file named example.py, 
# the variable __name__ would be set to example. 
# Here's an example of what that might look like:
#--------------------------------------------------------
#import app
#
#print("example __name__ = %s", __name__)

#if __name__ == "__main__":
#    print("example is being run directly.")
#else:
 #   print("example is being imported")
#--------------------------------------------------------

#We can define the welcome route using the code below:
@app.route("/")


#The next step is to add the routing information for each of the other routes.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#the naming convention /api/v1.0/ followed by the name of the route. 
# This convention signifies that this is version 1 of our application.
#  This line can be updated to support future versions of the app as well.
#----------------------
#To create the route, add the following code. 
# Make sure that it's aligned all the way to the left.
#9.5.3
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
#.\ to shorten length of your code so that it goes to the next line.

#9.5.4

#now it's time to move on to the third: the stations route.
#  For this route we'll simply return a list of all the stations.

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#9.5.5

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


#9.5.6
#this route is different from the previous ones 
#we will have to provide both a starting and ending date.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



#run flask--> this does not work
if __name__ == "__main__":
    app.run(debug=True)

