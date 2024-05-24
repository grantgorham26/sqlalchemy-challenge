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
    return '''Welcome to this API, its all about weather in Hawaii. In this API you will be able to access precipitation,temperature(tobs) data,
    the weather stations used to collect data. You can also set a date range and it will return the average, minimum and maximum temperature in that date range.<br/>
    


        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/start_date(yyyy-mm-dd)<br/>
        /api/v1.0/start_date(yyyy-mm-dd)/end_date(yyyy-mm-dd)
        
'''
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
    #Create list of dictionaries for precipitation data using list comprehension 
    precipitation_data = [{'date':date,'precipitation':prcp} for date, prcp in results]
   
    # print list in json form 
    session.close()
    return jsonify(precipitation_data)


#stations route 
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    #list of columns to query for station api
    sel = [Station.id,Station.station,Station.name, Station.latitude, Station.longitude, Station.elevation]
    results = session.query(*sel).all()
    #Create list of dictionaries for station data using list comprehension 
    station_data = [{'id':id, 'station':station, 'name':name, 'latitude':latitude, 'longitude':longitude, 'elevation':elevation}
                    for id, station, name, latitude, longitude, elevation in results]
    
    
        
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
    #Create list of dictionaries for temperature data using list comprehension 
    temperature_data = [{'station':station, 'date':date, 'temperature': tobs} for station, date, tobs in results_temp]
    

        
    session.close()
    return jsonify(temperature_data)

# #dynamic route start and end dates 
def get_temperature_stats(start, end=None):
    session = Session(engine)
    
    # Convert the start date parameter to datetime format
    start_date = datetime.strptime(start, '%Y-%m-%d')
    
    # Initialize query to filter by start date
    query = session.query(func.min(Measurement.tobs),
                            func.max(Measurement.tobs),
                            func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start_date)
    
    # If end date is provided, add filter for end date
    if end:
        end_date = datetime.strptime(end, '%Y-%m-%d')
        query = query.filter(Measurement.date <= end_date)
    
    # Execute the query
    temp_stats = query.first()
    
    session.close()

    # Unpack the tuple returned by the query
    min_temp, max_temp, avg_temp = temp_stats

    return jsonify({
        'Low Temperature': min_temp,
        'Highest Temperature': max_temp,
        'Average Temperature': avg_temp
    })

#route with no end date
@app.route('/api/v1.0/<start>')
def temperature_stats(start):
    return get_temperature_stats(start)
#route with start and end date
@app.route('/api/v1.0/<start>/<end>')
def temperature_stats_range(start, end):
    return get_temperature_stats(start, end)



if __name__ == "__main__":
    app.run(debug=True)