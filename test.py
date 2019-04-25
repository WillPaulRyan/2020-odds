import os

from flask import Flask, flash, jsonify, redirect, render_template, request
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import *
from application import timeConvert
from datetime import datetime

# Configure application
app = Flask(__name__)

engine = create_engine('postgres://jzqvuqvziqikpj:608cb6df0cb2c3258dfb5d06db73047dd710b5d698c90a81b8f25bf9dadaf9fe@ec2-107-20-177-161.compute-1.amazonaws.com:5432/d355cs90th9vsm')
connection = engine.connect()
metadata = MetaData()
election = Table('election', metadata, autoload = True, autoload_with=engine)

query = select([election]).order_by(desc(election.columns.datetime))

ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchone()

A = ResultSet

print (datetime.strftime(A[0], '%Y-%m-%d %H:%M:%S'))