# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
# Start at the homepage
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# convert precipitation analysis to database - return JSON
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data from the last 12 months"""
    # Query data from last 12 months
    rain_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    # Close session
    session.close()

    # Create a dictionary
    rain_data = []
    for date, prcp in rain_year:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        rain_data.append(rain_dict)

    # Return JSON
    return jsonify(rain_dict)

# return JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query stations
    station_names = session.query(Station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all stations
    all_stations = []
    for station in station_names:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)

# query dates and tobs of most active station - return JSON
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temperature opbservations for the most active station"""
    # Query all tobs
    year_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date >= '2016-08-23').all()

    session.close()

# Return JSON list of min, max, and avg for start and start/end date
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def <start>():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   temp_summary = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).group_by(Measurement.station).all()

    session.close()

if __name__ == '__main__':
    app.run(debug=True)
