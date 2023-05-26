#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 3 - servidor.py
Grupo: 33
Números de aluno: 56908, 56916
"""

import ast
from os.path import isfile
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import sqlite3, sqlite, requests, sqlite, json

app = Flask(__name__)

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

#Link das apis - 1
# API dos voos
URLF = "http://lmpinto.eu.pythonanywhere.com/roundtrip/ygyghjgjh/"
# API do tempo
URLW = "https://lmpinto.eu.pythonanywhere.com/v1/forecast.json?"

# formatar data
def format_date(date_str):
    # Parse the input date string
    date = datetime.fromisoformat(date_str[:-6])

    # Format the date string as "YYYY-MM-DD HHMM"
    return date.strftime("%Y-%m-%d %H%M")
  
# obter metereologia das proximas 2 semanas das cidades da base de dados
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
    
# obter voos de uma location para todas as opcoes possiveis  
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
    roundtrips = []
    legs_data = []
    for location in locations:
        arr = db.execute("Select * from locations where name = ?", [location[1]]).fetchone()[2]
        for date in dates:
            response = requests.get(URLF + f"{dep}/{arr}/{date[0]}/{date[1]}/1/0/0/Economy/EUR")
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

# obter detalhes de uma viagem, ou várias viagens, a partir do seu ID
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

# filtrar viagens para localização, companhia aérea e número de dias de sol
def filterTrips(location, airline, days_of_sun):
    trips, _ = getFlights(location, 999999999999)
    trips = getDetails([trip["id"] for trip in trips])
    
    filtered_trips = []
    
    for trip in trips:
        good_weather = 0
        if (trip["leg0"]["airlineCodes"][0] == trip["leg1"]["airlineCodes"][0]) and trip["leg0"]["airlineCodes"][0] == airline:
            for weather in trip["weather"].values():
                if weather in good_weather_conditions:
                    good_weather += 1
            if int(good_weather) == int(days_of_sun):
                filtered_trips.append(trip)
                
    return filtered_trips

# filtrar viagens por destino mais barato
def filterTripsDiversify(trips: list):
    filtered_trips = getDetails(trips)

    return filtered_trips

# 2
# ------------------------------ ROTAS ------------------------------

#rota search
@app.route('/search', methods=['GET'])
#função search da rota search
def search():
    location = request.args.get('location')
    cost = request.args.get('cost')
    
    weather = getWeather()
    flight_ids = [flight["id"] for flight in getFlights(location, cost)[0]]
    flights = getDetails(flight_ids)
    return jsonify(flights)

# rota filter
@app.route('/filter', methods=['GET'])
# função filter da rota filter
def filter():
    location = request.args.get('location')
    airline = request.args.get('airline')
    days_of_sun = request.args.get('days_of_sun')
    
    if int(days_of_sun) <= 4 or int(days_of_sun) >= 2:
        filtered_trips = filterTrips(location, airline, days_of_sun)
    else:
        return jsonify("Número de dias de sol inválido!")
    
    if filtered_trips:
        return jsonify(filtered_trips)
    else:
        return jsonify("Viagem não encontrada!")

# rota filter/diversify 
@app.route('/filter/diversify', methods=['GET'])
# função filter_diversify da rota filter/diversify
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

# rota details
@app.route('/details', methods=['GET'])
# função details da rota details
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
    app.run(debug=True, port=5000)
