import socket
import threading
import requests

def recibir_mensajes(sock):
    while True:
        data = sock.recv(1024).decode('utf-8')
        print('\nMensaje recibido:', data)

def enviar_mensaje(sock):
    while True:
        mensaje = input('Ingrese el mensaje a enviar: ')
        sock.sendall(mensaje.encode('utf-8'))

def obtener_direccion_ip_publica():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except socket.error:
        return None

def modo_servidorLAN():
    # Obtén la dirección IP de la computadora actual
    ip = socket.gethostbyname(socket.gethostname())

    # Crea un objeto de socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincula el socket a una dirección IP y un puerto
    sock.bind((ip, 5000))

    # Escucha las conexiones entrantes (puede aceptar hasta 1 conexión)
    sock.listen(1)

    print(f'Esperando conexión en {ip}:5000...')

    # Acepta una conexión entrante
    cliente_sock, cliente_dir = sock.accept()
    print('Cliente conectado:', cliente_dir)

    # Crea dos hilos para recibir y enviar mensajes
    recibir_hilo = threading.Thread(target=recibir_mensajes, args=(cliente_sock,))
    enviar_hilo = threading.Thread(target=enviar_mensaje, args=(cliente_sock,))

    # Inicia los hilos
    recibir_hilo.start()
    enviar_hilo.start()

def modo_servidorINTERNET():
    # Obtén la dirección IP pública antes de crear el socket
    ip = obtener_direccion_ip_publica()
    print(ip)

    # Si no se puede obtener la dirección IP pública, muestra un mensaje y regresa
    if ip is None:
        print('No se pudo obtener la dirección IP pública.')
        return

    # Crea un objeto de socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincula el socket a una dirección IP y un puerto
    sock.bind((ip, 8080))

    # Escucha las conexiones entrantes (puede aceptar hasta 1 conexión)
    sock.listen(1)

    print(f'Esperando conexión en {ip}:8080...')

    # Acepta una conexión entrante
    cliente_sock, cliente_dir = sock.accept()
    print('Cliente conectado:', cliente_dir)

    # Crea dos hilos para recibir y enviar mensajes
    recibir_hilo = threading.Thread(target=recibir_mensajes, args=(cliente_sock,))
    enviar_hilo = threading.Thread(target=enviar_mensaje, args=(cliente_sock,))

    # Inicia los hilos
    recibir_hilo.start()
    enviar_hilo.start()

def modo_cliente():
    ip_servidor = input('Ingrese la dirección IP del servidor: ')

    # Crea un objeto de socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta al servidor
        sock.connect((ip_servidor, 5000))
        print('Conectado al servidor')

        # Crea dos hilos para recibir y enviar mensajes
        recibir_hilo = threading.Thread(target=recibir_mensajes, args=(sock,))
        enviar_hilo = threading.Thread(target=enviar_mensaje, args=(sock,))

        # Inicia los hilos
        recibir_hilo.start()
        enviar_hilo.start()

    except ConnectionRefusedError:
        print('No se pudo conectar al servidor')

def modo_clienteINTERNET():
    ip_servidor = input('Ingrese la dirección IP del servidor: ')

    # Crea un objeto de socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta al servidor
        sock.connect((ip_servidor, 8080))
        print('Conectado al servidor')

        # Crea dos hilos para recibir y enviar mensajes
        recibir_hilo = threading.Thread(target=recibir_mensajes, args=(sock,))
        enviar_hilo = threading.Thread(target=enviar_mensaje, args=(sock,))

        # Inicia los hilos
        recibir_hilo.start()
        enviar_hilo.start()

    except ConnectionRefusedError:
        print('No se pudo conectar al servidor')

# Menú principal
print('--- Aplicación de Chat ---')
print('1. Modo Servidor')
print('2. Modo Cliente')
print('3. INTERNET')

opcion = input('Seleccione una opción: ')

if opcion == '1':
    modo_servidorLAN()
elif opcion == '2':
    modo_cliente()
elif opcion == '3':
    print('1. Modo Servidor')
    print('2. Modo Cliente')
    opcion1 = input('Seleccione una opción: ')
    if opcion1 == '1':
        modo_servidorINTERNET()
    elif opcion1 == '2':
        modo_cliente()
    else:
        print('Opción inválida')
else:
    print('Opción inválida')
