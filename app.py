import datetime as dt

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
Base.prepare(engine, reflect=True)

# Save reference to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"<br>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server recieved request for 'precipitation' page...")

    # Create session from Python to database
    session = Session(engine)

    # Perform a query to retrieve all date and precipitation values
    dt_and_prcp = session.query(measurement.date, measurement.prcp).all()

    # Close session
    session.close()

    # Convert query results to dictionary
    dt_and_prcp_dict = {}
    for date, prcp in dt_and_prcp:
        dt_and_prcp_dict[date] = prcp

    # Return JSON representation of your dictionary
    return jsonify(dt_and_prcp_dict)

@app_route("/api/v1.0/stations")
def stations():
    print("Server recieved request for 'stations' page...")

    # Create session from Python to database
    session = Session(engine)

    # Perform a query to retrieve all stations
    stations = session.query(station.station).all()

    # Close session
    session.close()

    # Return JSON list of stations from dataset
    return jsonify(stations)

@app_route("/api/v1.0/tobs")
def tobs():
    print("Server recieved request for 'tobs' (temperature observation) page...")

    # Create session from Python to database
    session = Session(engine)

    # Perform a query to retrieve tobs info for most active station
    most_active_sta = session.query(measurement.station, func.count(measurement.station)).\
                                    order_by(func.count(measurement.station).desc()).\
                                    group_by(measurement.station).\
                                    first()[0]

    # Identify the most recent date, and calculate one year ago date (365 days before last date)
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent_dt = (dt.datetime.strptime(most_recent, "%Y-%m-%d")).date()
    year_ago = most_recent_dt - dt.timedelta(days = 365)

    # Perform a query to retrieve the tobs for the last year
    most_active_tobs = session.query(measurement.date, measurement.tobs).\
        filter((measurement.station ==most_active_sta)\
        & measurement.date >=year_ago)\
        & (measurement.date <= most_recent_dt)).all()

    # Close session
    session.close()

    # Return JSON list of stations from dataset
    return jsonify(most_active_tobs)

@app_route("/api/v1.0/<start>")
def start():
