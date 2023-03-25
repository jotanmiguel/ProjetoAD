"""
Aplicações distribuídas - Projeto 2 - sock_utils.py
Grupo: 33
Números de aluno: 56908, 56916
"""
import socket as s

def create_tcp_server_socket(address, port, queue_size):
	"""
	Metodo para uma socket para o servidor TCP. 

	Args:
		address (str): ip.
		port (str): port.
		queue_size (int): queue size.

	Returns:
		socket: Socket criada.
	"""
	sock = s.socket(s.AF_INET, s.SOCK_STREAM)
	sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
	sock.bind((address, port))
	sock.listen(queue_size)
	return sock

def create_tcp_client_socket(address, port):
	"""
	Metodo para uma socket para o cliente TCP.

	Args:
		address (str): ip.
		port (str): port.

	Returns:
		socket: Socket criada.
	"""
	sock = s.socket(s.AF_INET, s.SOCK_STREAM)
	return sock

def receive_all(socket, length):
	"""
	Metodo para receber todos os bytes da ligação.

	Args:
		socket (socket): Socket a ser usada.
		length (int): Tamanho da mensagem, em bytes, a ser recebida.

	Returns:
		bytes: bytes a receber do socket.
	"""
	msg = ''
	while len(msg) < length:
		ms = socket.recv(length - len(msg))
		msg+=ms
	return msg