#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 4 - servidor.py
Grupo: 33
Números de aluno: 56908, 56916
"""

import ast
from functools import wraps
import os
from os.path import isfile
from datetime import datetime, timedelta
import secrets
import ssl
import sqlite3
import requests
import json
import sqlite
from flask import Flask, make_response, redirect, request, jsonify, session, url_for
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import id_token
from google.auth.transport import requests as transport
from kazoo.client import KazooClient

app = Flask(__name__)
zk = KazooClient(hosts='localhost:2181')

def connect_db(dbname):
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row
    return db

# condicoes para bom tempo
good_weather_conditions = [
    "Clear",
    "Sunny",
    "Mostly sunny",
    "Partly cloudy",
    "Mostly clear",
    "Scattered clouds",
    "Few clouds",
    "Fair",
    "Pleasant",
    "Mild"
]
dates = [((datetime.strptime('2023-04-26', '%Y-%m-%d') + timedelta(days=x)).strftime("%Y-%m-%d"), (datetime.strptime('2023-04-26', '%Y-%m-%d') + timedelta(days=(x + 3))).strftime("%Y-%m-%d")) for x in range(0, 11)]

URLF = "http://lmpinto.eu.pythonanywhere.com/roundtrip/ygyghjgjh/"
URLW = "https://lmpinto.eu.pythonanywhere.com/v1/forecast.json?"

def format_date(date_str):
    # Parse the input date string
    date = datetime.fromisoformat(date_str[:-6])

    # Format the date string as "YYYY-MM-DD HHMM"
    return date.strftime("%Y-%m-%d %H%M")
    
def getWeather():
    db = connect_db("BD.db")
    locations = [location[1] for location in db.execute("SELECT * FROM locations").fetchall()]
    weather_data = []
    for location in locations:
        response = requests.get(URLW + f"q={location}&days=14")
        if response.status_code == 200:
            weather = response.json()["forecast"]["forecastday"]
            last_id = db.execute("SELECT MAX(id) FROM weather").fetchone()[0] or 0
            for day in weather:
                date = day["date"]
                maxtemp = day["day"]["maxtemp_c"]
                mintemp = day["day"]["mintemp_c"]
                condition = day["day"]["condition"]["text"]
                # Check if weather data for this date and location already exists
                existing_data = db.execute("SELECT * FROM weather WHERE date=? AND location=?", (date, location)).fetchone()
                if not existing_data:
                    # Insert weather data into database
                    last_id += 1
                    db.execute("INSERT INTO weather (id, date, location, condition, mintemp_c, maxtemp_c) VALUES (?, ?, ?, ?, ?, ?)",
                                (last_id, date, location, condition, int(mintemp), int(maxtemp)))
                    weather_data.append({"id":last_id, "date":date, "location":location, "condition":condition, "mintemp":int(mintemp), "maxtemp":int(maxtemp)})
                else:
                    # Use existing weather data if it already exists in the database
                    weather_data.append((list(existing_data)))
    db.commit()
    db.close()
    return weather_data
    
def getFlights(location:str, cost:int):
    """_summary_

    Args:
        location (str): _description_
        cost (int): _description_

    Returns:
        _type_: _description_
    """
    db = connect_db("BD.db")
    db.execute("DELETE FROM roundtrips")
    db.execute("DELETE FROM legs")
    dep = db.execute("Select * from locations where name = ?", [location]).fetchone()[2]
    locations = db.execute("SELECT * FROM locations").fetchall()
    print(dep, [location[1] for location in locations])
    roundtrips = []
    legs_data = []
    for location in locations:
        arr = db.execute("Select * from locations where name = ?", [location[1]]).fetchone()[2]
        for date in dates:
            response = requests.get(URLF + f"{dep}/{arr}/{date[0]}/{date[1]}/1/0/0/Economy/EUR")
            print(response.url)
            if response.status_code == 200:
                fares, trips, legs = response.json()["fares"], response.json()["trips"], response.json()["legs"]
                for leg,fare in zip(legs, fares):
                    if int(fare["price"]["amount"]) <= int(cost) and leg["stopoverCode"] == "DIRECT":
                        legId = leg["id"]
                        departureAirportCode = leg["departureAirportCode"]
                        arrivalAirportCode = leg["arrivalAirportCode"]
                        departureDatetime = leg["departureDateTime"]
                        arrivalDatetime = leg["arrivalDateTime"]
                        durationMinutes = leg["durationMinutes"]
                        airlines = str(leg["airlineCodes"])
                        legs_data.append({legId, departureAirportCode, arrivalAirportCode, departureDatetime, arrivalDatetime, durationMinutes, airlines})
                        existing_leg = db.execute("SELECT id FROM legs WHERE id=?", [legId]).fetchone()
                        if existing_leg is None:
                            legs_data.append({legId, departureAirportCode, arrivalAirportCode, departureDatetime, arrivalDatetime, durationMinutes, airlines})
                            db.execute("INSERT INTO legs VALUES (?, ?, ?, ?, ?, ?, ?)", (legId, departureAirportCode, arrivalAirportCode, departureDatetime, arrivalDatetime, durationMinutes, airlines))
                            db.commit()
                for leg, fare, trip in zip(legs_data, fares, trips):
                    # Get the IDs of the legs in the roundtrip
                    leg_id_0, leg_id_1 = trip["legIds"][0], trip["legIds"][1]                
                    
                    # Look up the legs in the legs table by their IDs
                    leg_0 = db.execute("SELECT * FROM legs WHERE id=?", [leg_id_0]).fetchone()
                    leg_1 = db.execute("SELECT * FROM legs WHERE id=?", [leg_id_1]).fetchone()
                    if leg_0 is not None and leg_1 is not None and not db.execute("SELECT EXISTS(SELECT 1 FROM roundtrips WHERE id=?)", [trip["id"]]).fetchone()[0]:
                        roundtrips.append({"id":trip["id"], "cost":fare["price"]["amount"], "id_leg0":dict(leg_0)["id"], "id_leg1":dict(leg_1)["id"]})
                        db.execute("INSERT INTO roundtrips (id, cost, id_leg0, id_leg1) VALUES (?, ?, ?, ?)", (trip["id"], fare["price"]["amount"], dict(leg_0)["id"], dict(leg_1)["id"]))
                        db.commit()
    db.close()
    return roundtrips, legs_data

def getDetails(viagem_ids:list):
    """
    Obter detalhes de uma viagem, ou várias viagens, a partir do seu ID.

    Args:
        viagem_ids (list): lista de ids de viagens.

    Returns:
        list: lista de objetos com os detalhes das viagens.
    """
    db = connect_db("BD.db")    
    roundtrips = [{"id":roundtrip["id"], "cost":roundtrip["cost"], "id_leg0":roundtrip["id_leg0"], "id_leg1":roundtrip["id_leg1"]} for roundtrip in db.execute("SELECT * FROM roundtrips").fetchall()]
    legs = [{"legId":leg["id"], "dep_IATA":leg["dep_IATA"], "arr_IATA":leg["arr_IATA"], "dep_datetime":leg["dep_datetime"], "arr_datetime":leg["arr_datetime"], "duration_min":leg["duration_min"], "airlineCodes":ast.literal_eval(leg["airlineCodes"])} for leg in db.execute("SELECT * FROM legs").fetchall()]
    locations = [{"id":location["id"], "name":location["name"], "IATA":location["IATA"], "wea_name":location["wea_name"]} for location in db.execute("SELECT * FROM locations").fetchall()]    
    weather = [{"id":weather["id"], "date":weather["date"], "location":weather["location"], "condition":weather["condition"], "mintemp_c":weather["mintemp_c"], "maxtemp_c":weather["maxtemp_c"]} for weather in db.execute("SELECT * FROM weather").fetchall()]    
    
    trips = []
    for id in viagem_ids:
        if id in [roundtrip["id"] for roundtrip in roundtrips]:
            roundtrip = [roundtrip for roundtrip in roundtrips if roundtrip["id"] == id][0]
            leg0 = [leg for leg in legs if leg["legId"] == roundtrip["id_leg0"]][0]
            leg1 = [leg for leg in legs if leg["legId"] == roundtrip["id_leg1"]][0]
            dst = [location for location in locations if location["IATA"] == leg0["arr_IATA"]][0]
            weather_data = {}
            for w in weather:
                if w["location"] == dst["wea_name"] and w["date"] >= leg0["arr_datetime"][:10] and w["date"] <= leg1["dep_datetime"][:10]:
                    weather_data[str(len(weather_data))] = w["condition"]
            trips.append({"cost":roundtrip["cost"], "dst":leg0["arr_IATA"],"leg0":leg0, "leg1":leg1, "src":leg0["dep_IATA"], "trip_id":id, "weather":weather_data})
    
    db.close()
    return trips   

def filterTrips(search_id: int, location=None, airline=None, days_of_sun=None):
    db = connect_db("BD.db")

    # Retrieve the trip IDs associated with the search ID from the search_trips table
    trip_ids = db.execute("SELECT trip_ids FROM search_trips WHERE search_id = ?", (search_id,)).fetchone()
    if not trip_ids:
        db.close()
        return "No search available!"
    
    trip_ids = trip_ids[0].split(", ")

    # Get the trip details for the retrieved trip IDs
    trips = getDetails(trip_ids)
    filtered_trips = []

    db.close()
    
    if all(param is None for param in [location, airline, days_of_sun]):
        filtered_trips = trips
        return filtered_trips
    else:
        filtered_trips = []
        for trip in trips:
            if (not location or location == trip["dst"]) and (not airline or airline in trip["leg0"]["airlineCodes"]):
                good_weather = 0
                for weather in trip["weather"].values():
                    if weather in good_weather_conditions:
                        good_weather += 1
                if not days_of_sun or int(good_weather) == int(days_of_sun):
                    filtered_trips.append(trip)

        db.close()

    return filtered_trips

def filterTripsDiversify(trips: list):
    filtered_trips = getDetails(trips)

    return filtered_trips

# Google OAuth 2 configuration
CLIENT_SECRETS_FILE = 'client/client_secret_486662482266-2hi4up7rsabt8sodrpm44qtr2i5bf54k.apps.googleusercontent.com.json'
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = 'https://localhost:5000/callback'

app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    print(session.get('credentials'))
    return make_response('Bem vindo à escapadinha solarenga!')

@app.route('/login')
def login():
    auth_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    return redirect(auth_url, code=302)

@app.route('/callback')
def callback():
    #auth_url, state = flow.authorization_url(prompt='consent')
    code = request.args.get("code")

    flow.fetch_token(code=code)
    
    session['client_id'] = flow.credentials.client_id
    session['credentials'] = flow.credentials.to_json()

    with open('token.json', 'w') as token_file:
        token_file.write(flow.credentials.to_json())
        
    return "Logged in successfully!"

@app.route('/logout')
def logout():
    session.pop('credentials')
    os.remove('token.json')
    return "Logged out successfully!"

def login_required(view_func):
    """
    Decorator that redirects to the login page if the user is not authenticated.
    """
    @wraps(view_func)
    def decorated_func(*args, **kwargs):
        # Check if the user is authenticated
        if 'credentials' not in session:
            return "Unauthorized. Please /login"  # Redirect to the login page
        return view_func(*args, **kwargs)
    
    return decorated_func

@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    pass

@app.route('/search', methods=['GET'])
@login_required
def search():
    location = request.args.get('location')
    cost = request.args.get('cost')
    
    db = connect_db("BD.db")
    results = db.execute("Select * FROM searches").fetchall()
    search_id = len(results)
    # Check if the search has already been performed by the current user
    existing_search = db.execute("SELECT * FROM searches WHERE client_id=? AND search_params=?", (session['client_id'], f"location={location}&cost={cost}")).fetchone()
    
    flight_ids = [flight["id"] for flight in getFlights(location, cost)[0]]

    if not existing_search:
        db.execute("INSERT INTO searches (search_id, client_id, search_params) VALUES (?, ?, ?)", (search_id, session['client_id'], f"location={location}&cost={cost}"))
        db.commit()
        getWeather()
        db.execute("INSERT INTO search_trips (search_id, trip_ids) VALUES (?, ?)", (search_id, ', '.join(flight_ids)))
        db.commit()
        search_id += 1
        db.close()
        flights = getDetails(flight_ids)
        return jsonify({'search id':search_id, 'trips':flights})
    else: 
        flights = getDetails(flight_ids)
        db.close()
        return jsonify({'search id':search_id, 'trips':flights})

    

@app.route('/filter', methods=['GET'])
@login_required
def filter():
    search_id = request.args.get('s_id')
    location = request.args.get('location')
    airline = request.args.get('airline')
    days_of_sun = request.args.get('days_of_sun')
    
    if days_of_sun:
        if int(days_of_sun) <= 4 or int(days_of_sun) >= 2:
            filtered_trips = filterTrips(int(search_id), location, airline, days_of_sun)
        else:
            return jsonify("Número de dias de sol inválido!")
    else:
        filtered_trips = filterTrips(int(search_id), location, airline, days_of_sun)
    
    if filtered_trips:
        return jsonify(filtered_trips)
    else:
        return jsonify("Sem viagens!")

#passar para a funcao filterTripsDiversity  
@app.route('/filter/diversify', methods=['GET'])
@login_required
def filter_diversify():       
    trip_ids = request.args.getlist('trip_ids')[0].split(',')
    trips = getDetails(trip_ids)
    
    filtered_trips = {}

    for trip in trips:
        dst = trip['dst']
        cost = trip['cost']
        if dst not in filtered_trips or cost < filtered_trips[dst]['cost']:
            filtered_trips[dst] = trip

    return jsonify(list(filtered_trips.values()))


@app.route('/details', methods=['GET'])
@login_required
def details():
    viagem_id = [request.args.get('trip_id')]
    
    viagem_details = getDetails(viagem_id)
    if viagem_details:
        return jsonify(viagem_details)
    else:
        return jsonify("Viagem não encontrada!")

if __name__ == '__main__':
    db,_ = sqlite.connect_db("BD.db")
    getWeather()
    db.close()
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='certs/root.pem')
    context.load_cert_chain(certfile='server/serv.crt',keyfile='server/serv.key')
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    app.run('localhost', ssl_context=context, debug = True)
