import requests
import json
import os
import subprocess

while True:

    comandosSup = ['CREATE','READ','DELETE','UPDATE']

    inputLinha = input("Comando: ")
    args = inputLinha.split()
    comando = args[0].upper()
    token = "BQD_I_a8bEs7FW_whd8iLWRmulCXu4W-AwFoKlbycaKFMAM1-e4KKPhSy_9vCn7tODUxScZJSxW9odrLjKQAZK6n-LqiQd15LFe5tgK48j1nGYOKR2W98ZObBkRKC8QuWESERRtDu3qBqJUhzCVt"
    if comando in comandosSup:

        if comando == "CREATE":
            if args[1].upper() == "UTILIZADOR":
                if len(args) < 4:
                    print("MISSING ARGUMENTS")
                else:
                    print(args)
                    dados = {'nome':str(args[2]),'senha':str(args[3])} 
                    r = requests.post('http://localhost:5000/utilizadores', json = dados)

            elif args[1].upper() == "ARTISTA":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    artistName =str("https://api.spotify.com/v1/artists/"+args[2]+"")
                    spotify = os.popen('curl -X "GET" '+artistName+' -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')
                    spot = json.loads(spotify.read())
                    dados = {"id_spotify":str(args[2]),"nome":spot["name"]} 
                    r = requests.post('http://localhost:5000/artistas', json = dados)

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
                    dados = {'user':args[1],'musica':str(args[2]),'avaliacao':str(args[3])}
                    r = requests.post('http://localhost:5000/playlist', json = dados) 

                    


    #         elif comando == "UNLOCK":
    #             if len(args) < 3:
    #                 print("MISSING ARGUMENTS")
    #             else:
    #                 cliente.connect()
    #                 resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2]+' '+ ID)
    #                 print('Resposta: %s' % resposta)
    #                 cliente.close()

    #         elif comando == 'STATUS':
    #             if len(args) < 2:
    #                 print("MISSING ARGUMENTS")
    #             else:
    #                 cliente.connect()
    #                 resposta = cliente.send_receive(args[0] +' '+ args[1])
    #                 print('Resposta: %s' % resposta)
    #                 cliente.close()

    #         elif comando == 'STATS':
    #             if len(args) < 2:
    #                 print("MISSING ARGUMENTS")
    #             elif args[1].upper() in ['K','N','D']:
    #                 if args[1].upper() == 'K':
    #                         if len(args) < 3:
    #                             print("MISSING ARGUMENTS")
    #                         else:
    #                             cliente.connect()
    #                             resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2])
    #                             print('Resposta: %s' % resposta)
    #                             cliente.close()
    #                 else:
    #                         if len(args) < 2:
    #                             print("MISSING ARGUMENTS")
    #                         else:
    #                             cliente.connect()
    #                             resposta = cliente.send_receive(args[0] +' '+ args[1])
    #                             print('Resposta: %s' % resposta)
    #                             cliente.close()

    #         elif comando == "PRINT":
    #                 cliente.connect()
    #                 resposta = cliente.send_receive(args[0])
    #                 print('Resposta: %s' % resposta)
    #                 cliente.close()
                
    #     else:
    #         print("UNKNOWN COMMAND")



    # r = requests.get('http://localhost:5000/aluno/25')
    # print (r.status_code)
    # print (r.content.decode())
    # print (r.headers)
    # print ('***')
    # dados = {'numero': 123, 'nome': 'Carabino Tiro Certo', 'idade': 18}
    # r = requests.put('http://localhost:5000/aluno', json = dados)
    # print (r.status_code)
    # print (r.content.decode())
    # print (r.headers)
    # print ('***')
    # notas = {'numero_aluno': 123, 'ano': '2018/2019', 'cadeira': 'AD', 'nota': 20}
    # r = requests.post('http://localhost:5000/notas', json = notas)
    # print (r.status_code)
    # print (r.content.decode())
    # print (r.headers)
    # print ('***')
    # pesquisa = {'ano': '2018/2019', 'cadeira': 'AD'}
    # r = requests.get('http://localhost:5000/notas', json = pesquisa)
    # print (r.status_code)
    # print (r.content.decode())
    # print (r.headers)
    # print ('***')
    # r = requests.get('http://localhost:5000/aluno/123')
    # print (r.status_code)
    # print (r.content.decode())
    # print (r.headers)
    # print ('***')