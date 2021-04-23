import socket
import hashlib
import threading
FILE100 = "prueba100mb.txt"
FILE250 = "prueba250mb.txt"
FILEPRUEBA = "prueba.txt"


# Método que define el tamanio del file a trabajar
def menu_inicial_tamanio():
    file_name = ""
    print("presione el número del archivo que desea ejecutar"
          "\n" "1. 100Mb"
          "\n" "2. 250Mb"
          "\n" "3. archivo de texto de ejemplo"
          "\n" "4. archivo propio")
    file_size: str = input()
    try:
        file_tamanio = int(file_size)
    except:
        print("no se ingresó un valor numerico")
    if file_tamanio < 0 or file_tamanio > 4:
        print("por favor ingrese un número entre 1 y 4")
        print(file_size)
        menu_inicial_tamanio()
    if file_size == "1":
        file_name = FILE100
    if file_size == "2":
        file_name = FILE250
    if file_size == "3":
        file_name = FILEPRUEBA
    if file_size == "4":
        print("inserte el nombre del archivo localizado en la carpeta files"
              "\n" "El nombre del archivo debe de ir completo incluyendo su extensión "
              "\n" "Ej. prueba1gb.txt")
        file_name = input()
        print("El nombre de su archivo es: " + file_name)
    return file_tamanio, file_name


# Método que define el número de conexiones con las que se van a trabajar
def menu_inicial_conexiones():
    print("Inserte el número de conexiones deseadas (1-25): ")
    conexiones = input()
    connections = int(conexiones)
    if connections > 25 or connections < 1:
        print("por favor ingrese un número entre 1 y 25")
        menu_inicial_conexiones()
    return connections


# Se crea el socket de tipo UDP
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser_socket.bind(('127.0.0.1', 12345))
# Se define el número de clientes con los que se va a trabajar
conexiones = menu_inicial_conexiones()
# Se captura el número del archivo y su nombre en caso de ser necesario
numero, nombre = menu_inicial_tamanio()


def hasheame_esta():
    """"This function returns the SHA-1 hash
       of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open("files/" + nombre, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


# se envía el nombre del archivo al cliente


def send_file_name(addr):
    if numero == 1:
        ser_socket.sendto(FILE100.encode('utf-8'), addr)
    if numero == 2:
        ser_socket.sendto(FILE250.encode('utf-8'), addr)
    if numero == 3:
        ser_socket.sendto(FILEPRUEBA.encode('utf-8'), addr)
    if numero == 4:
        ruta = nombre
        print(ruta)
        ser_socket.sendto(ruta.encode('utf-8'), addr)



# Se calcula el hash
hexadecimal = hasheame_esta()


def mandar_file(addr):
    f = open("files/" + nombre, 'rb')
    l = f.read(1024)
    datagramas = 0
    print("enviando el archivo " + nombre)
    print("el hash del archivo es: " + hexadecimal)
    while l:
        datagramas += 1
        ser_socket.sendto(l, addr)
        l = f.read(1024)
    print("se Finalizó el envio del archivo")
    corte = nombre + "kill"
    # Se envía 4 veces la orden de terminar la recepción de archivos (ya que por UDP hay perdida de datagramas)
    ser_socket.sendto(corte.encode('utf-8'), addr)
    ser_socket.sendto(corte.encode('utf-8'), addr)
    ser_socket.sendto(corte.encode('utf-8'), addr)
    ser_socket.sendto(corte.encode('utf-8'), addr)


# Se recibe la información de conexión del cliente
def esperar_conexiones():
    esperadas = 0
    while esperadas < conexiones:
        try:
            data, addr = ser_socket.recvfrom(1024)
            #se manda el nombre
            thread_x = threading.Thread(target=send_file_name(addr))
            #se manda el hash
            thread_y = threading.Thread(target=send_file_name(addr))
            #se manda el file
            thread_z = threading.Thread(target=mandar_file(addr))
        except OSError as err:
            print(err)

        esperadas += 1


esperar_conexiones()
