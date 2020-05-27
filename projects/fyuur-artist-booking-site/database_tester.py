import sys
from flask import Flask, render_template, request, redirect, jsonify, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
import dateutil.parser
import datetime
import babel


# app setup, db setup
engine = create_engine(
    'postgresql://postgres:password@localhost:5432/fyuurapp')
connection = engine.connect()

metadata = MetaData()

#venue = Table('Venue', metadata, autoload=True, autoload_with=engine)

stmt = 'select start_time from "Show";'

result_p = connection.execute(stmt)
results = result_p.fetchall()

print()
