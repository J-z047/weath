# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import statistics
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(autoload_with=engine)
# reflect an existing database into a new model

# reflect the tables


# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# Define the home route
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation data<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the most active station<br/>"
        f"/api/v1.0/<start> - Temperature statistics from a start date (YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end> - Temperature statistics between start and end date (YYYY-MM-DD)"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query date and prcp from the Measurement table for the last year
    last_year = dt.date.today() - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= last_year).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query all station names from the Station table
    results = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    station_list = []
    for station, name in results:
        station_dict = {
            "station": station,
            "name": name
        }
        station_list.append(station_dict)
    
    return jsonify(station_list)

# Add other routes for "tobs", temperature statistics from start and end dates, etc.

if __name__ == "__main__":
    app.run(debug=True)