import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify, render_template, request

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

query_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/yyyy-mm-dd<br/>"
    f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > query_date).group_by(Measurement.date).all()
    all_rain = []
    for rain in results:
        rain_dict = {}
        rain_dict["Date"] = rain.date
        rain_dict["Rain"] = rain.prcp
        all_rain.append(rain_dict)
    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    all_tobs = []
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date).all()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>/")
def start_temp(start):

    results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date == start).all()
    results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start).all()
    results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start).all()
    trip_start = {"Min Temp" : results_min, "Max Temp" : results_max, "Average Temp" : results_avg}
    return jsonify(trip_start)

@app.route("/api/v1.0/<start>/<end>/")
def temps(start, end):

    temp_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end ).all()
    temp_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end ).all()
    temp_avg= session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end ).all()
  
    trip = {"Min Temp" : temp_min, "Max Temp" : temp_max, "Average Temp" : temp_avg}
    return jsonify(trip)

if __name__ == "__main__":
    app.run(debug=True)
