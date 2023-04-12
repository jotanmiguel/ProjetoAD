# from flask import Flask, request, jsonify
# import sqlite3

# app = Flask(__name__)

# def create_database():
#     # Implemente a criação e inicialização do banco de dados aqui

# def get_database_connection():
#     conn = sqlite3.connect('database.db')
#     return conn

# @app.route('/search', methods=['GET'])
# def search():
#     location = request.args.get('location')
#     cost = request.args.get('cost')

#     # Implemente a busca por viagens usando a API weatherapi.com e flightapi.io aqui

#     return jsonify(viagens_encontradas)

# @app.route('/filter', methods=['POST'])
# def filter():
#     data = request.get_json()
#     viagem_ids = data['viagem_ids']
#     location = data.get('location')
#     airline = data.get('airline')
#     sun = data.get('sun')

#     # Implemente a filtragem das viagens aqui

#     return jsonify(viagens_filtradas)

# @app.route('/details', methods=['GET'])
# def details():
#     viagem_id = request.args.get('viagem_id')

#     # Implemente a busca de detalhes da viagem aqui

#     return jsonify(viagem_details)

# if __name__ == '__main__':
#     create_database()
#     app.run(debug=True)
