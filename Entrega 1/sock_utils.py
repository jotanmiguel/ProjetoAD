"""
Aplicações distribuídas - Projeto 1 - sock_utils.py
Grupo: 
Números de aluno: 56908, 
"""
import socket as s

def create_tcp_server_socket(address, port, queue_size):
	sock = s.socket(s.AF_INET, s.SOCK_STREAM)
	sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
	sock.bind((address, port))
	sock.listen(queue_size)
	return sock

def create_tcp_client_socket(address, port):
	sock = s.socket(s.AF_INET, s.SOCK_STREAM)
	return sock

def receive_all(socket, length):
	msg = ''
	while len(msg) < length:
		ms = socket.recv(length - len(msg))
		msg+=ms
	return msg