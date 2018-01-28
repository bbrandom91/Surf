import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation observations from previous year<br/>"
        f"/api/v1.0/stations - List of stations from dataset<br/>"
        f"/api/v1.0/tobs - Temperature observations from previous year<br/>"
        f"/api/v1.0/<start> - Returns Max, Min, and Average temperature for dates after start<br/>"
        f"/api/v1.0/<start>/<end> - Returns Max, Min, and Average temperature for dates after start and before end <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
	result = engine.execute("SELECT date, prcp FROM measurement WHERE date > '2017-01-01' AND date < '2018-01-01'")
	precip_dict = {r.date : r.prcp for r in result}
	return jsonify([precip_dict])

@app.route("/api/v1.0/stations")
def stations():
	result = engine.execute(" SELECT station from station ")
	station_list = [r.station for r in result]
	stations_dict = {"station list": station_list}
	return jsonify([stations_dict])

@app.route("/api/v1.0/tobs")
def tobs():
	result = engine.execute(" SELECT date, tobs FROM measurement WHERE date > '2017-01-01' AND date < '2018-01-01' ")
	temp_dict = {r.date : r.tobs for r in result}
	return jsonify([temp_dict])

@app.route("/api/v1.0/<start>")
def start_from(start):
	query = "SELECT MAX(tobs) AS max_temp, MIN(tobs) AS min_temp, AVG(tobs) AS avg_temp FROM measurement WHERE date >= '%s' "%(start)
	result = engine.execute(query)
	temp_return_list = [[r.max_temp, r.min_temp, r.avg_temp] for r in result  ][0]
	temp_return_dict = { "Max Temperature": temp_return_list[0], "Min Temperature": temp_return_list[1], "Average Temperature": temp_return_list[2] }
	return jsonify([start,temp_return_dict])

@app.route("/api/v1.0/<start>/<end>")
def start_stop(start,end):
	query = "SELECT MAX(tobs) AS max_temp, MIN(tobs) AS min_temp, AVG(tobs) AS avg_temp FROM measurement WHERE date >= '%s' AND date <= '%s' "%(start, end)
	result = engine.execute(query)
	temp_return_list = [[r.max_temp, r.min_temp, r.avg_temp] for r in result  ][0]
	temp_return_dict = { "Max Temperature": temp_return_list[0], "Min Temperature": temp_return_list[1], "Average Temperature": temp_return_list[2] }
	return jsonify([(start,end),temp_return_dict])


if __name__ == "__main__":
    app.run(debug=True)








