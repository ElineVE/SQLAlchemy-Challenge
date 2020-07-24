
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br//>"
        f"/api/v1.0/<start>:<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    

    """Return a list of all Measurement names"""
    # Query all categories
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)



@app.route("/api/v1.0/stations")
def stations():
    

    """Return a list of all Station names"""
    # Query all categories
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
    

    #set the latest date
    startdate = datetime(2016, 8, 23)

    # Query all date and tobs values
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= startdate).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list of tobs
    alltobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        alltobs.append(tobs_dict)

    return jsonify(alltobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start = None, end = None):
  

    #set the dates
    startdate = start
    
    start = datetime.strptime(startdate, "%Y-%m-%d")
    if (end):
        end = datetime.strptime(end, "%Y-%m-%d")


    # Query all date and tobs values
    results = session.query(func.min(Measurement.tobs).label('MinTemp'), func.avg(Measurement.tobs).label('AvgTemp'), func.max(Measurement.tobs).label('MaxTemp')).\
        filter(Measurement.date >= start).all()
        #.filter(Measurement.date <= end_date)

    session.close()

    # Create a dictionary from the row data and append to a list of tobs
    all_stats = []
    for MinTemp, AvgTemp, MaxTemp in results:
        stats_dict = {}
        stats_dict[MinTemp] = MinTemp
        stats_dict[AvgTemp] = AvgTemp
        stats_dict[MaxTemp] = MaxTemp
        all_stats.append(stats_dict)

    return jsonify(all_stats)


if __name__ == '__main__':
    app.run(debug=True)
