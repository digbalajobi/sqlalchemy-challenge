# import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

from flask import Flask, jsonify

# Database Setup
#################################################
#creating engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect Database & Tables
Base = automap_base()
Base.prepare(engine, reflect=True)


# Save table references 
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session
session = Session(engine)

inspector = inspect(engine)
inspector.get_table_names()


# Flask Setup
#################################################
app = Flask(__name__)

#Flask Routes

@app.route("/")
def home():
     return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    print("Precipitation API Request recieved")
    
    # query session for precipitation data (PD)
    session=Session(engine)
    results_p = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Dictionary list
    PD = []
    for result in results:
        precipDict = {result.date: result.prcp, "Station": result.station}
        PD.append(precipDict)

    
    return  jsonify(PD)


@app.route("/api/v1.0/stations")
def station():
    print("Stations API Request recieved")
    
    # query station's list
    session=Session(engine)
    results_s = session.query(Station.station, Station.name).all()
    session.close()

    # Dictionary list
    stationData = []
    for station, name in results_s:
        station_dict = {}
        station_dict['Station'] = station
        station_dict['Name'] = name
        stationData.append(station_dict)

    return jsonify(stationData)


@app.route("/api/v1.0/tobs")
def tobs():
    #Temperature observed for the previous year
    print("Tobs API request recieved")
    
    # query session for temperature data
    session = Session(engine)

    results_t = session.query(Station.name, Measurement.station, Measurement.date,\
        Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >='2016-08-23').all()
    session.close()


    tobs_tempdata = []
    for t in results_t:
        tobs_dict = {}
        tobs_dict['Station'] = t[0]
        tobs_dict['Name'] = t[1]
        tobs_dict['Date'] = t[2]
        tobs_dict['Temperature'] = t[3]
        tobs_tempdata.append(tobs_dict)

    # jsonify the dictionary
    return jsonify(    tobs_tempdata = []
)

@app.route("/api/v1.0/<start>")
def start(start):
    
    print("Start Range API request recieved")

    # query for temperature data for input date
    session = Session(engine)
    min_date = session.query(Measurement.date, func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    max_date = session.query(Measurement.date, func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    avg_date = session.query(Measurement.date, func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    start_date = []
    
    #Adding min, max and aveg. temps into dictionary and append list

    for x in min_date:
        min_dict = {}
        min_dict['Min Temperature Date'] = x[0]
        min_dict['Min Temperature'] = x[1]
        start_list.append(min_dict)
    
    for x in max_date:
        max_dict = {}
        max_dict['Max Temperature Date'] = x[0]
        max_dict['Max Temperature'] = x[1]
        start_list.append(max_dict)
    
    for x in avg_date:
        avg_dict = {}
        avg_dict['Avg. Temperature Date'] = x[0]
        avg_dict['Avg. Temperature'] = x[1]
        start_list.append(avg_dict)
    
    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    print("Start and End Range API request recieved")

    # query for temperature data for input date
    session = Session(engine)
    range_min = session.query(Measurement.date, func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    range_max = session.query(Measurement.date, func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    range_avg = session.query(Measurement.date, func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    range_list = []
    
    #Adding min, max and aveg. temps into dictionary and append list

    for x in range_min:
        min_dict = {}
        min_dict['Min Temp Date'] = x[0]
        min_dict['Min Temp'] = x[1]
        range_list.append(min_dict)
    
    for x in range_max:
        max_dict = {}
        max_dict['Max Temp Date'] = x[0]
        max_dict['Max Temp'] = x[1]
        range_list.append(max_dict)
    
    for x in range_avg:
        avg_dict = {}
        avg_dict['Avg Temp Date'] = x[0]
        avg_dict['Avg Temp'] = x[1]
        range_list.append(avg_dict)
    
    return jsonify(range_list)

if __name__ == "__main__":
    app.run(debug=True)