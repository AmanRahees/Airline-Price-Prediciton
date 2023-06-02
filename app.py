from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import pickle
import numpy as np
import pandas as pd
import sklearn

app = Flask(__name__, static_folder='static')
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.post('/predict')
def Output_page():
    # get the data
    origin = request.form['from']
    destination = request.form['to']
    airline = request.form['Airline']
    stopage = request.form['stopage']
    departure = request.form['departure']
    arrival = request.form['arrival']

    # Convert departure 
    dept_day = int(pd.to_datetime(departure, format="%Y-%m-%dT%H:%M").day)
    dept_month = int(pd.to_datetime(departure, format ="%Y-%m-%dT%H:%M").month)
    dept_hour = int(pd.to_datetime(departure, format ="%Y-%m-%dT%H:%M").hour)
    dept_min = int(pd.to_datetime(departure, format ="%Y-%m-%dT%H:%M").minute)

    # Convert Arrival
    arrival_hour = int(pd.to_datetime(arrival, format ="%Y-%m-%dT%H:%M").hour)
    arrival_min = int(pd.to_datetime(arrival, format ="%Y-%m-%dT%H:%M").minute)

    # Duration
    dur_hour = abs(arrival_hour - dept_hour)
    dur_min = abs(arrival_min - dept_min)

    # concating
    inputs = [ airline, origin, destination, stopage, dept_day, dept_month, arrival_hour, arrival_min, dept_hour, dept_min, dur_hour, dur_min]

    # get price using model
    prediction = model.predict([inputs])
    price = round(prediction[0],2)
    dept = datetime.strptime(departure, '%Y-%m-%dT%H:%M')
    arrive = datetime.strptime(arrival, '%Y-%m-%dT%H:%M')
    context = {
        'airline': airline,
        'origin': origin,
        'destination': destination,
        'stopage': stopage,
        'dept_time': dept.strftime('%I:%M %p'),
        'dept_date': dept.strftime('%Y-%m-%d'),
        'arrive_time': arrive.strftime('%I:%M %p'),
        'arrive_date': arrive.strftime('%Y-%m-%d'),
        'price': price
    }
    return render_template('output.html', **context)

if __name__ == "__main__":
    app.run()