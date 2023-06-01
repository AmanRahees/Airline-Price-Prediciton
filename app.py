from flask import Flask, render_template, url_for, request
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
    input_data = np.asarray(inputs)
    final_input = input_data.reshape(1,-1)

    # get price using model
    prediction = model.predict(final_input)
    price = round(prediction[0],2)

    context = {
        'airline': airline,
        'origin': origin,
        'destination': destination,
        'stopage': stopage,
        'dept': departure,
        'arrival': arrival,
        'price': price
    }
    return render_template('output.html', context=context)
