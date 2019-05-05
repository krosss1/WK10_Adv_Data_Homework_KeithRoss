import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlite3
from flask import Flask, jsonify,g

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# print(Base.classes.measurement)
Measurements = Base.classes.measurement
Stations = Base.classes.station
session = Session(engine)
Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Please choose your start date and end date between 2010-01-01 and 2017-08-23 for the following search<br/>"
        f"/api/v1.0/:start_date<br/>"
        f"/api/v1.0/:start_date/:end_date"
    )

@app.route("/api/v1.0/precipitation")
def lastyearprec():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_prec = session.query(Measurements.date,Measurements.prcp).filter(Measurements.date >= last_year).\
     order_by(Measurements.date).all()
    prec_dict = [r._asdict() for r in last_year_prec]
    return jsonify(prec_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Stations.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def lastyeartemp():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_tobs = session.query(Measurements.date,Measurements.tobs).filter(Measurements.date >= last_year).\
    order_by(Measurements.date).all()
    tobs_dict = [r._asdict() for r in last_year_tobs]
    return jsonify(tobs_dict)

@app.route("/api/v1.0/")
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    start = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start_date).all()
    for record in start:
        (tmin, tave, tmax) = record
        return jsonify(min_temp=tmin,ave_temp=tave,max_temp=tmax)

@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date,end_date):
    start_end = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
    for record in start_end:
        (tmin, tave, tmax) = record
        return jsonify(min_temp=tmin,ave_temp=tave,max_temp=tmax)

if __name__ == "__main__":
    app.run(debug=True)