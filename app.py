# Import the functions we need from flask
from flask import Flask
from flask import render_template 
from flask import jsonify
from flask import request

# Import the functions we need from SQL Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, text

from config import username
from config import password
from config import API_KEY

from datetime import datetime

import math


# Define the database connection parameters
database_name = 'hurricanes' 
connection_string = f'postgresql://{username}:{password}@localhost:5432/{database_name}'

# Connect to the database
engine = create_engine(connection_string)
base = automap_base()
base.prepare(engine, reflect=True)

# Choose the table we wish to use
hurricane_table = base.classes.hurricanes

# Instantiate the Flask application. (Chocolate cake recipe.)
# This statement is required for Flask to do its job. 
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Effectively disables page caching

# Here's where we define the various application routes ...
@app.route("/")
def IndexRoute():
    ''' This function runs when the browser loads the index route. 
        Note that the html file must be located in a folder called templates. '''

    webpage = render_template("index.html")
    return webpage

@app.route("/other")
def OtherRoute():
    ''' This function runs when the user clicks the link for the other page.
        Note that the html file must be located in a folder called templates. '''

    # Note that this call to render template passes in the title parameter. 
    # That title parameter is a 'Shirley' variable that could be called anything 
    # we want. But, since we're using it to specify the page title, we call it 
    # what we do. The name has to match the parameter used in other.html. 
    webpage = render_template("other.html")
    return webpage

def build_sql_filter(year, name, city, country, category, wind, minwind, ocean):
    
    conds = []

    ### Comment this to use the full database
    #string = [hurricane_table.date_stamp/10000 >= "{}".format(1950)]
    #conds = conds + string

    if (year):
        string = [hurricane_table.date_stamp/10000 == "{}".format(year)]
        print(string)
        conds = conds + string

    if (name):
        string = [hurricane_table.name == "{}".format(name)]
        print(string)
        conds = conds + string

    if (city):
        string = [hurricane_table.city == "{}".format(city)]
        print(string)
        conds = conds + string

    if (country):
        string = [hurricane_table.country == "{}".format(country)]
        print(string)
        conds = conds + string

    if (category):
        string = [hurricane_table.category == "{}".format(category)]
        print(string)
        conds = conds + string

    if (wind):
        string = [hurricane_table.wind == "{}".format(wind)]
        print(string)
        conds = conds + string
    
    if (minwind):
        string = [hurricane_table.wind >= "{}".format(minwind)]
        print(string)
        conds = conds + string

    if (ocean):
        string = [hurricane_table.ocean == "{}".format(ocean)]
        print(string)
        conds = conds + string

    return conds


@app.route("/searchFor")
def searchFor():
    ''' Query the database for population numbers and return the results as a JSON. '''

    year  = request.args.get('year', None)
    name  = request.args.get('name', None)
    city = request.args.get('city', None)
    country = request.args.get('country', None)
    category = request.args.get('category', None)
    wind = request.args.get('wind', None)
    minwind = request.args.get('minwind', None)
    ocean = request.args.get('ocean', None)

    conds = []
    conds = build_sql_filter(year, name, city, country, category, wind, minwind, ocean)
    #conds = [ hurricane_table.date_stamp/10000 == '2005', hurricane_table.name == 'KATRINA' ]
    print(conds)

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(hurricane_table.name,
                            hurricane_table.date_stamp,
                            hurricane_table.time_stamp,
                            hurricane_table.status,
                            hurricane_table.wind,
                            hurricane_table.city,
                            hurricane_table.country,
                            hurricane_table.new_latitude,
                            hurricane_table.new_longitude,
                            hurricane_table.category,
                            hurricane_table.ocean)\
                                .filter(and_(*conds)).all()                                
                               
    session.close 

    print("Search Results: ", results)

    hurricaneDetails = []
    for name, date_stamp, time_stamp, status, wind, city, country, new_latitude, new_longitude, category, ocean in results:
        dict = {}
        dict["name"] = name
        dict["status"] = status
        dict["date_stamp"] = date_stamp
        dict["time_stamp"] = time_stamp
        dict["wind"] = wind
        dict["city"] = city
        dict["country"] = country
        dict["latitude"] = new_latitude
        dict["longitude"] = new_longitude
        dict["category"] = category
        dict["ocean"] = ocean
        hurricaneDetails.append(dict)

    # Return the jsonified result. 
    return jsonify(hurricaneDetails)


@app.route("/searchForUnique")
def searchForUnique():
    ''' Query the database for population numbers and return the results as a JSON. '''

    ### REQUIRED ###
    specific  = request.args.get('type', None)  

    ### OPTIONAL ###
    year  = request.args.get('year', None)
    name  = request.args.get('name', None)
    city = request.args.get('city', None)
    country = request.args.get('country', None)
    category = request.args.get('category', None)
    wind = request.args.get('wind', None)
    minwind = request.args.get('minwind', None)
    ocean = request.args.get('ocean', None)

    conds = []
    conds = build_sql_filter(year, name, city, country, category, wind, minwind, ocean)
    print(conds)

    # Open a session, run the query, and then close the session again
    session = Session(engine)

    if (specific == "year"):
        results = session.query(hurricane_table.date_stamp).filter(and_(*conds)).all()
    if (specific == "date"):
        results = session.query(hurricane_table.date_stamp).filter(and_(*conds)).all()
    if (specific == "name"):
        results = session.query(hurricane_table.name).filter(and_(*conds)).all()
    if (specific == "city"):
        results = session.query(hurricane_table.city).filter(and_(*conds)).all()
    if (specific == "country"):
        results = session.query(hurricane_table.country).filter(and_(*conds)).all()
    if (specific == "wind"):
        results = session.query(hurricane_table.wind).filter(and_(*conds)).all()
    if (specific == "minwind"):
        results = session.query(hurricane_table.wind).filter(and_(*conds)).all()
    if (specific == "category"):
        results = session.query(hurricane_table.category).filter(and_(*conds)).all()
    if (specific == "ocean"):
        results = session.query(hurricane_table.ocean).filter(and_(*conds)).all()

    session.close          

    List = []

    if (specific == "year"):
        for row in results:
            yearNum = math.floor(row[0] / 10000)
            if (yearNum not in List):
                List.append(yearNum)
    else:
        for row in results:
            if (row[0] not in List):
                List.append(row[0])

    #print("Search Results: ", results)
    #print("Search List: ", List)

    List.sort()

    if (specific == "year"):
        List.sort(reverse=True)


    outboundJson = []

    for element in List:

        dict = {}
        if (specific == "year"):
            dict["year"] = element
        if (specific == "date"):
            dict["date_stamp"] = element
        if (specific == "name"):
            dict["name"] = element
        if (specific == "city"):
            dict["city"] = element
        if (specific == "country"):
            dict["country"] = element
        if (specific == "wind"):
            dict["wind"] = element
        if (specific == "minwind"):
            dict["minwind"] = element
        if (specific == "category"):
            dict["category"] = element
        if (specific == "ocean"):
            dict["ocean"] = element

        outboundJson.append(dict)

    # Return the jsonified result. 
    return jsonify(outboundJson)


@app.route("/yearData")
def YearData():

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(hurricane_table.date_stamp).all()
    session.close 

    yearData = []
    for date_stamp in results:
        date_time_str = str(date_stamp[0])
        date_time_obj = datetime.strptime(date_time_str, '%Y%m%d')
        date_time_year = date_time_obj.year
        if date_time_year not in yearData:
            yearData.append(date_time_year)

    yearData.sort(reverse=True)

    yearJson = []
    for year in yearData:
        dict = {}
        dict["year"] = year
        #print("yearValue: ", date_time_obj.year)
        yearJson.append(dict)

    # Return the jsonified result. 
    #return jsonify(yearData)
    return jsonify(yearJson)

@app.route("/nameData")
def NameData():

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(hurricane_table.name).all()
    session.close 

    nameData = []
    for name in results:
        name_str = str(name[0])
        if name_str not in nameData:
            nameData.append(name_str)

    nameData.sort()

    nameJson = []
    for name in nameData:
        dict = {}
        dict["name"] = name        
        if dict not in nameJson:
            nameJson.append(dict)

    # Return the jsonified result. 
    return jsonify(nameJson)

# This statement is required for Flask to do its job. 
# Think of it as chocolate cake recipe. 
if __name__ == '__main__':
    app.run(debug=True)