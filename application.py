import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request
import requests
import sqlite3
from oddscalculator import DecimalOdds, AmericanOdds
from datetime import datetime, timedelta


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

db = SQL("    postgres://jzqvuqvziqikpj:608cb6df0cb2c3258dfb5d06db73047dd710b5d698c90a81b8f25bf9dadaf9fe@ec2-107-20-177-161.compute-1.amazonaws.com:5432/d355cs90th9vsm?sslmode=require")


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


def convertToStrings(A):
    """Convert list of ints into proper odds format"""

    for thing in A:
        try:
            if A[thing] >= 0:
                A[thing] = '+' + str(A[thing])
            else:
                A[thing] = str(A[thing])
        except:
            pass
    return (A)


def lookup():
    """Look up odds"""

    # Connect to database

    # Pull most recent entry
    currentData = db.execute("SELECT * FROM election ORDER BY datetime DESC LIMIT 1")[0]

    # Date testing info
    timeFormat = '%Y-%m-%d %H:%M:%S'
    timeNow = datetime.strftime(datetime.utcnow(), timeFormat)
    timeLimit = timedelta(days=2)
    timeElapsed = datetime.strptime(timeNow, timeFormat) - datetime.strptime(currentData['datetime'], timeFormat)

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
        db.executemany("INSERT INTO election(datetime, trump, warren, booker, biden, sanders, klobuchar, harris, gillibrand, gabbard, orourke, yang, buttigieg, castro) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [oddsValues])

        # Return values in an array
        return oddsValues

    else:

        # Return previous values in an array
        return currentData


def timeConvert(time):
    """Convert time to a better format"""

    FMTin = '%Y-%m-%d %H:%M:%S'
    FMTout = '%m/%d/%y'

    return datetime.strftime(datetime.strptime(time, FMTin), FMTout)

@app.route("/")
def index():
    """Show odds"""

    oddsInfo = convertToStrings(lookup())
    oddsInfo['datetime'] = timeConvert(oddsInfo['datetime'])

    return render_template("index.html", oddsInfo=oddsInfo)