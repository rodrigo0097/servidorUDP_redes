import socket
import hashlib
"""
data, addr = cli_socket.recvfrom(4096)
print("Server Says")
print(str(data))
cli_socket.close()
"""
cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = "Hello"
cli_socket.sendto(msg.encode("utf-8"), ('127.0.0.1', 12345))
data,addr = cli_socket.recvfrom(1024)
numero_conexiones = data.decode('utf-8')
data,addr = cli_socket.recvfrom(1024)
# Se captura el nombre del file desde el servidor
file_name = data
titulo = file_name.decode("utf-8")
f = open("ArchivosRecibidos/"+titulo, 'wb')
# recepción del hash
data,addr = cli_socket.recvfrom(1024)
hexadecimal_hash = data.decode()

def hasheame_esta():
    """"This function returns the SHA-1 hash
       of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open("files/"+titulo, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


print("Nicole y brayan: el número de sockets que deben crear en esta iteración es " + numero_conexiones)
print(file_name)
print("se recibe el archivo con un hash esperado de " + hexadecimal_hash)
print(numero_conexiones)

data,addr = cli_socket.recvfrom(1024)
corte = titulo + "kill"
termine = corte.encode('utf-8')
print("se recibe el archivo" + titulo)
while data != termine:
    f.write(data)
    data,addr = cli_socket.recvfrom(1024)
print("archivo recibido")
f.close()
