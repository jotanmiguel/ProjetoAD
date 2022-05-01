#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Aplicações Distribuídas - Projeto 3 - client.py
Grupo: 2
Números de aluno: 56908, 56954
"""

import requests
import json
import os
import subprocess

while True:

    comandosSup = ['CREATE','READ','DELETE','UPDATE']

    inputLinha = input("Comando: ")
    args = inputLinha.split()
    comando = args[0].upper()
    token = "BQBT-DZyI5ssoY3scGImotFJCHsNrdOsqWwau3NCQsBHf493CUrJL3caRcKritXjqXgaiSJFovn2xItrd8G5MAqejHWoqyiXURVFkSqIC8XSMe-tlihiyaecz1bb8BG7U6V4QEhHaCYwaABIw5BW"

    if comando in comandosSup:

        if comando == "CREATE":
            if args[1].upper() == "UTILIZADOR":
                if len(args) < 4:
                    print("MISSING ARGUMENTS")
                else:
                    dados = {'nome':str(args[2]),'senha':str(args[3])} 
                    r = requests.post('http://localhost:5000/utilizadores', json = dados)
                    print (r.content.decode())   

            elif args[1].upper() == "ARTISTA":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    artistName =str("https://api.spotify.com/v1/artists/"+args[2]+"")
                    spotify = os.popen('curl -X "GET" '+artistName+' -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')
                    spot = json.loads(spotify.read())
                    dados = {"id_spotify":str(args[2]),"nome":spot["name"]} 
                    r = requests.post('http://localhost:5000/artistas', json = dados)
                    print (r.content.decode())   

            elif args[1].upper() == "MUSICA":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    songName =str("https://api.spotify.com/v1/tracks/"+args[2]+"?market=ES")
                    spotify = os.popen('curl -X "GET" '+songName+' -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')
                    spot = json.loads(spotify.read())
                    dados = {"id_spotify":str(args[2]),"nome":spot["name"],"id_artista":spot["artists"][0]["id"],"token":token} 
 
                    r = requests.post('http://localhost:5000/musicas', json = dados)
            else:
                if len(args) < 4:
                    print("MISSING ARGUMENTS")
                else:
                    dados = {'user':args[1],'musica':args[2],'avaliacao':str(args[3])}
                    r = requests.post('http://localhost:5000/playlist', json = dados)
                    print (r.content.decode())   

        elif comando == "READ":
            if args[1].upper() == "UTILIZADOR":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    r = requests.get('http://localhost:5000/utilizadores/'+args[2])
                    print (r.status_code)
                    print (r.content.decode())
            elif args[1].upper() == "ARTISTA":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    r = requests.get('http://localhost:5000/artistas/'+str(args[2]))
                    print (r.status_code)
                    print (r.content.decode())
            elif args[1].upper() == "MUSICA":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    r = requests.get('http://localhost:5000/musicas/'+str(args[2]))
                    print (r.status_code)
                    print (r.content.decode())
            elif args[1].upper() == "ALL":
                if args[2].upper() in ["UTILIZADORES","ARTISTAS","MUSICAS"] and len(args) < 4:
                    dados = {'tipo':args[2].upper()}
                    r = requests.get('http://localhost:5000/', json = dados)
                    print (r.status_code)
                    print (r.content.decode()) 
                else:
                    dados = {'tipo':args[2].upper(),'extra':args[3]}
                    r = requests.get('http://localhost:5000/', json = dados)
                    print (r.status_code)
                    print (r.content.decode())
                
        elif comando == "DELETE":
            if args[1].upper() == "UTILIZADOR":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    r = requests.delete('http://localhost:5000/utilizadores/'+args[2])
                    print (r.status_code)
                    print (r.content.decode())
            elif args[1].upper() == "ARTISTA":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    r = requests.delete('http://localhost:5000/artistas/'+str(args[2]))
                    print (r.status_code)
                    print (r.content.decode())
            elif args[1].upper() == "MUSICA":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    r = requests.delete('http://localhost:5000/musicas/'+str(args[2]))
                    print (r.status_code)
                    print (r.content.decode())
            elif args[1].upper() == "ALL":
                if args[2].upper() in ["UTILIZADORES","ARTISTAS","MUSICAS"] and len(args) < 4:
                    dados = {'tipo':args[2].upper()}
                    r = requests.delete('http://localhost:5000/', json = dados)
                    print (r.status_code)
                    print (r.content.decode()) 
                else:
                    dados = {'tipo':args[2].upper(),'extra':args[3]}
                    r = requests.delete('http://localhost:5000/', json = dados)
                    print (r.status_code)
                    print (r.content.decode())
        
        elif comando == "UPDATE":
            if args[1].upper() == "MUSICA":
                if len(args) < 5:
                    print("MISSING ARGUMENTS")
                else:
                    dados = {'id_musica':str(args[2]),'avaliacao':str(args[3]),'id_user':str(args[4])}                     
                    r = requests.put('http://localhost:5000/playlist', json = dados)
                    print (r.status_code)
                    print (r.content.decode())
            elif args[1].upper() == "UTILIZADOR":
                if len(args) < 4:
                    print("MISSING ARGUMENTS")
                else:
                    dados = {'id_user':str(args[2]),'password':str(args[3])}                     
                    r = requests.put('http://localhost:5000/utilizadores/'+str(args[2]), json = dados)
                    print (r.status_code)
                    print (r.content.decode()) 
    else:
        print("INAVLID COMMAND")           


                             



                    