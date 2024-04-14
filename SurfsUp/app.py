# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import timedelta, datetime


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
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)






#################################################
# Flask Routes
#################################################


#creating welcome page
@app.route('/')
def welcome():
    
    #list all routes 
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start_date(yyyy-mm-dd)<br/>'
        f'/api/v1.0/start_date(yyyy-mm-dd)/end_date(yyyy-mm-dd)'
        
    )
#precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    #find the most recent day recorded
    recent_rain = session.query(Measurement).filter(Measurement.date).\
        order_by(Measurement.date.desc()).first()    
    # Starting from the most recent data point in the database. 
    start_date_str = recent_rain.date
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    # Calculate the date one year from the last date in data set.
    end_date = start_date - timedelta(days=365)
    
    #query date and precipitation with the wanted params
    results = session.query(Measurement.date,Measurement.prcp).\
                      filter(Measurement.date <= start_date_str,
                      Measurement.date >= end_date.strftime('%Y-%m-%d')).all()
    #create list to put dictionary of data into
    precipitation_data = []
    for date, prcp in results:
    #create empty dictionary for date and precipitaion 
        precipitation_dict = {}
        precipitation_dict['date']= date
        precipitation_dict['precipitation'] = prcp
        precipitation_data.append(precipitation_dict)
    # print list in json form 
    session.close()
    return jsonify(precipitation_data)


#stations route 
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    #list of columns to query for statin api
    sel = [Station.id,Station.station,Station.name, Station.latitude, Station.longitude, Station.elevation]
    results = session.query(*sel).all()
    station_data = []
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['id'] = id
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        station_data.append(station_dict)
        session.close()
    return jsonify(station_data)

# temperature route
@app.route('/api/v1.0/tobs')
def temperatures():
    session = Session(engine)
    #define variables that will be used
    #find the most recent day recorded
    recent_rain = session.query(Measurement).filter(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    # Starting from the most recent data point in the database. 
    start_date_str = recent_rain.date
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    # Calculate the date one year from the last date in data set.
    end_date = start_date - timedelta(days=365)

    #get only the most active station
    observation_counts = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    most_active_station = observation_counts[0][0]


    #query station id, date and temp with the wanted params
    results_temp = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                      filter(Measurement.date <= start_date_str,
                      Measurement.date >= end_date.strftime('%Y-%m-%d'),
                      Measurement.station == most_active_station).all()
    #create list to put dictionary of data into
    temperature_data = []
    for station, date, tobs in results_temp:
#create empty dictionary for date and precipitaion 
        temperature_dict = {}
        temperature_dict['station'] = station
        temperature_dict['date']= date
        temperature_dict['temperature'] = tobs
        temperature_data.append(temperature_dict)
        session.close()
    return jsonify(temperature_data)

#dynamic route start and end dates 
@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session(engine)
    if start is None:
        return "Please provide a start date parameter in the URL.", 400
    

    
    min_temp = session.query(Measurement.tobs, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()[0][0]
    max_temp = session.query(Measurement.tobs, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()[0][0]
    avg_temp = session.query(Measurement.tobs, func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()[0][0]

    session.close()

    return jsonify ({'Low Temperature': min_temp,
                     'Highest Temperature': max_temp,
                     'Average Temperature': avg_temp
                     
                    })

    


@app.route('/api/v1.0/<start>/<end>')

def start_date_end_date(start,end):
    session = Session(engine)
    if start is None:
        return "Please provide a start date parameter in the URL.", 400
    

    min_temp = session.query(Measurement.tobs, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()[0][0]
    max_temp = session.query(Measurement.tobs, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()[0][0]
    avg_temp = session.query(Measurement.tobs, func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()[0][0]

    session.close()

    return jsonify ({'Low Temperature': min_temp,
                     'Highest Temperature': max_temp,
                     'Average Temperature': avg_temp
                     
                    })


if __name__ == "__main__":
    app.run(debug=True)