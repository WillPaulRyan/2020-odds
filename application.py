import os

from flask import Flask, flash, jsonify, redirect, render_template, request
import flask_sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
from oddscalculator import DecimalOdds, AmericanOdds
from datetime import datetime, timedelta
from sqlalchemy import Column, create_engine, DateTime, desc, Integer, MetaData, select, Table
from NewLog import NewLog

from helpers import candidateSort, convertToStrings, timeConvert

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

    
def call():
    """Call the API"""

    # Contact API
    try:
        response = requests.get("http://api.betdata.io/live?market=us-presidential-election-2020")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        pull = response.json()
        return pull["data"]
    except requests.exceptions.RequestException as e:
        return e


def lookup():
    """Look up odds"""

    # Connect to database
    engine = create_engine('postgres://jzqvuqvziqikpj:608cb6df0cb2c3258dfb5d06db73047dd710b5d698c90a81b8f25bf9dadaf9fe@ec2-107-20-177-161.compute-1.amazonaws.com:5432/d355cs90th9vsm')
    connection = engine.connect()
    metadata = MetaData()
    election = Table('election', metadata, autoload = True, autoload_with=engine)

    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()    

    # Pull most recent entry
    query = select([election]).order_by(desc(election.columns.timestamp)) # VS Code says "election" has an error, but it doesn't
    ResultProxy = connection.execute(query)
    proxy = ResultProxy.fetchone()

    # Date testing info
    timeFormat = '%Y-%m-%d %H:%M:%S'
    oldTime = datetime.strftime(proxy[0], timeFormat)
    timeNow = datetime.strftime(datetime.utcnow(), timeFormat)
    timeLimit = timedelta(days=2)
    timeElapsed = datetime.strptime(timeNow, timeFormat) - datetime.strptime(oldTime, timeFormat)

    # If greater than two days old
    if timeElapsed >= timeLimit:

        # Use call() function to get data
        newData = call()

        # Begin conversion to American Odds
        trump = DecimalOdds(newData["donaldtrump"][1])
        warren = DecimalOdds(newData["elizabethwarren"][1])
        booker = DecimalOdds(newData["corybooker"][1])
        biden = DecimalOdds(newData["joebiden"][1])
        sanders = DecimalOdds(newData["berniesanders"][1])
        klobuchar = DecimalOdds(newData["amyklobuchar"][1])
        harris = DecimalOdds(newData["kamalaharris"][1])
        gillibrand = DecimalOdds(newData["kirstengillibrand"][1])
        gabbard = DecimalOdds(newData["tulsigabbard"][1])
        orourke = DecimalOdds(newData["betoorourke"][1])
        yang = DecimalOdds(newData["andrewyang"][1])
        buttigieg = DecimalOdds(newData["petebuttigieg"][1])
        castro = DecimalOdds(newData["juliancastro"][1])

        # Finish conversion and prepare data to be put in database
        oddsValues = [timeNow, int(trump.american), int(warren.american), int(booker.american), int(biden.american), int(sanders.american), int(klobuchar.american), int(harris.american), int(gillibrand.american), int(gabbard.american), int(orourke.american), int(yang.american), int(buttigieg.american), int(castro.american)]

        # Insert data into database
        session.add(NewLog(timestamp = timeNow, trump = oddsValues[1], warren = oddsValues[2], booker = oddsValues[3], biden = oddsValues[4], sanders = oddsValues[5], klobuchar = oddsValues[6], harris = oddsValues[7], gillibrand = oddsValues[8], gabbard = oddsValues[9], orourke = oddsValues[10], yang = oddsValues[11], buttigieg = oddsValues[12], castro = oddsValues[13]))
        session.commit()
        session.flush()
        
        # Return values in an array
        session.close()
        return oddsValues

    else:
        # Put data in usable format
        currentData = [oldTime]
        for column in proxy[1:]:
            currentData = currentData + [column]

        # Return previous values in an array
        session.close()
        return currentData



@app.route("/")
def index():
    """Show odds"""

    updateDate, oddsInfo = candidateSort(lookup())

    return render_template("index.html", updateDate=timeConvert(updateDate), oddsInfo=convertToStrings(oddsInfo))