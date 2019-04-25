import os

from flask import Flask, flash, jsonify, redirect, render_template, request
from oddscalculator import AmericanOdds, DecimalOdds
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from NewLog import NewLog
from datetime import datetime, timedelta

from application import timeConvert


# Configure application
newData = {"donaldtrump":["Donald Trump",2.36],"mikepence":["Mike Pence",135],"timkaine":["Tim Kaine",1000],"paulryan":["Paul Ryan",845],"andrewcuomo":["Andrew Cuomo",340],"elizabethwarren":["Elizabeth Warren",49.5],"juliancastro":["Julian Castro",700],"michelleobama":["Michelle Obama",430],"corybooker":["Cory Booker",145],"joebiden":["Joe Biden",9.3],"marcorubio":["Marco Rubio",1000],"hillaryclinton":["Hillary Clinton",220],"berniesanders":["Bernie Sanders",8.1],"michaelbloomberg":["Michael Bloomberg",490],"amyklobuchar":["Amy Klobuchar",285],"johnkasich":["John Kasich",535],"tedcruz":["Ted Cruz",1000],"nikkihaley":["Nikki Haley",325],"newtgingrich":["Newt Gingrich",1000],"treygowdy":["Trey Gowdy",1000],"kamalaharris":["Kamala Harris",14.75],"markzuckerberg":["Mark Zuckerberg",1000],"markcuban":["Mark Cuban",1000],"algore":["Al Gore",1000],"carolinekennedy":["Caroline Kennedy",1000],"ivankatrump":["Ivanka Trump",760],"catherinecortezmasto":["Catherine Cortez Masto",1000],"kanyewest":["Kanye West",1000],"johnhickenlooper":["John Hickenlooper",790],"dannelmalloy":["Dannel Malloy",1000],"jayinslee":["Jay Inslee",865],"markdayton":["Mark Dayton",1000],"oprahwinfrey":["Oprah Winfrey",675],"kenbone":["Ken Bone",1000],"dwaynejohnson":["Dwayne Johnson",350],"ericgarcetti":["Eric Garcetti",1000],"howardschultz":["Howard Schultz",485],"johndelaney":["John Delaney",830],"sallyyates":["Sally Yates",1000],"devalpatrick":["Deval Patrick",1000],"bobiger":["Bob Iger",1000],"evanmcmullin":["Evan McMullin",1000],"gavinnewsom":["Gavin Newsom",1000],"johnkerry":["John Kerry",1000],"kirstengillibrand":["Kirsten Gillibrand",310],"alfranken":["Al Franken",1000],"timryan":["Tim Ryan",645],"stevebullock":["Steve Bullock",430],"roycooper":["Roy Cooper",1000],"sherrodbrown":["Sherrod Brown",1000],"martinomalley":["Martin O'Malley",1000],"tulsigabbard":["Tulsi Gabbard",90],"dougjones":["Doug Jones",1000],"mittromney":["Mitt Romney",855],"ninaturner":["Nina Turner",1000],"georgeclooney":["George Clooney",1000],"condoleezzarice":["Condoleezza Rice",1000],"jasonkander":["Jason Kander",1000],"michaelavenatti":["Michael Avenatti",1000],"tomcotton":["Tom Cotton",1000],"bensasse":["Ben Sasse",780],"ericholder":["Eric Holder",1000],"johnmcafee":["John McAfee",1000],"candaceowens":["Candace Owens",765],"stephanieclifford":["Stephanie Clifford",1000],"maggiehassan":["Maggie Hassan",1000],"elonmusk":["Elon Musk",1000],"betoorourke":["Beto O'Rourke",26],"billdeblasio":["Bill de Blasio",1000],"rahmemanuel":["Rahm Emanuel",1000],"oscardelahoya":["Oscar De La Hoya",1000],"sarahpalin":["Sarah Palin",965],"andrewgillum":["Andrew Gillum",1000],"richardojeda":["Richard Ojeda",1000],"ericswalwell":["Eric Swalwell",360],"andrewyang":["Andrew Yang",34],"tomsteyer":["Tom Steyer",1000],"jamesmattis":["James Mattis",1000],"angelinajolie":["Angelina Jolie",1000],"joekennedy":["Joe Kennedy",1000],"alexandriaocasiocortez":["Alexandria Ocasio-Cortez",500],"larryhogan":["Larry Hogan",1000],"petebuttigieg":["Pete Buttigieg",13.75],"staceyabrams":["Stacey Abrams",340],"terrymcauliffe":["Terry McAuliffe",1000],"waynemessam":["Wayne Messam",1000],"billweld":["Bill Weld",1000]}

# Set up Postgres data
engine = create_engine('postgres://jzqvuqvziqikpj:608cb6df0cb2c3258dfb5d06db73047dd710b5d698c90a81b8f25bf9dadaf9fe@ec2-107-20-177-161.compute-1.amazonaws.com:5432/d355cs90th9vsm')
connection = engine.connect()
metadata = MetaData()
election = Table('election', metadata, autoload = True, autoload_with=engine)

# create a configured "Session" class
Session = sessionmaker(bind=engine)
# create a Session
session = Session()

query = select([election]).order_by(desc(election.columns.timestamp))
ResultProxy = connection.execute(query)
proxy = ResultProxy.fetchone()


# Date testing info
timeFormat = '%Y-%m-%d %H:%M:%S'
oldTime = datetime.strftime(proxy[0], timeFormat)
timeNow = datetime.strftime(datetime.utcnow(), timeFormat)
timeLimit = timedelta(days=2)
timeElapsed = datetime.strptime(timeNow, timeFormat) - datetime.strptime(oldTime, timeFormat)


currentData = [oldTime]
for column in proxy[1:]:
    currentData = currentData + [column]

#currentData[0] = oldTime

print (currentData)