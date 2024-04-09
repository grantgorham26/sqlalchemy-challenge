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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
# session = Session(engine)

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
    session = Session(engine)
    #list all routes 
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>'
    )
# precipitation route
# @app.route('/api/v1.0/precipitation')
# def precipitation():
#     #find the most recent day recorded
#     recent_rain = session.query(Measurement).filter(Measurement.date).\
#         order_by(Measurement.date.desc()).first()
# # Starting from the most recent data point in the database. 
#     start_date_str = recent_rain.date
#     start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
# # Calculate the date one year from the last date in data set.
#     end_date = start_date - timedelta(days=365)
# #query date and precipitation with the wanted params
#     results = session.query(Measurement.date,Measurement.prcp).\
#                       filter(Measurement.date <= start_date_str,
#                       Measurement.date >= end_date.strftime('%Y-%m-%d')).all()
#     precipitation_data = []
#     for date, prcp in results:
#         precipitation_dict = {}
#         precipitation_dict['date']= date
#         precipitation_dict['precipitatin'] = prcp
#         precipitation_data.append(precipitation_dict)
#     return jsonify(precipitation_data)

#stations route 
# @app.route('/api/v1.0/stations')
# def stations():
#     return

# #temperature route
# @app.route('/api/v1.0/tobs')
# def temperatures():
#     return

# #dynamic route start and end dates 
# @app.route('/api/v1.0/<start>')
# def start_date():
#     return


# @app.route('/api/v1.0/<start>/<end>')
# def start_end_date():
#     return

