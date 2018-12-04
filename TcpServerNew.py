import socket

h = open('index.php', 'r')
homepage = h.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)    

s.bind(('', 8000))
s.listen(5)

# while True:
#     conn, addr = s.accept()
#     data = conn.recv(2000)

#     if 'GET' in data.decode():

#         conn.sendall('Hello word'.encode())
#         dataParse = data.decode().split(' ')

#         if dataParse[1] == '/':
#             conn.sendall(('HTTP/1.0 200 OK\r\n' +
#                       'Content-Type: text/html\r\n' +
#                       'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' +
#                       (homepage)).encode())
#         else:
#             ext = dataParse[1].rpartition(".")[-1]
#             f = open(dataParse[1][1:], 'r+b')
#             figure = f.read()
#             conn.sendall(('HTTP/1.0 200 OK\r\n' +
#                           'Content-Type: image' + ext + '\r\n' +
#                           'Content-Length: ' + str(len(figure)) + '\r\n\r\n').encode() +
#                           (figure))

#     conn.close()

def setIndex():
  while True:
   conn, addr = s.accept()
   data = conn.recv(2000)
   if not data:
      break

   if 'GET' in data.decode():

        #conn.sendall('Hello word'.encode())
        dataParse = data.decode().split(' ')

        if dataParse[1] == '/':
            conn.sendall(('HTTP/1.0 200 OK\r\n' +
                      'Content-Type: text/html\r\n' +
                      'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' +
                      (homepage)).encode())
        else:
            ext = dataParse[1].rpartition(".")[-1]
            f = open(dataParse[1][1:], 'r+b')
            figure = f.read()
            conn.sendall(('HTTP/1.0 200 OK\r\n' +
                          'Content-Type: image' + ext + '\r\n' +
                          'Content-Length: ' + str(len(figure)) + '\r\n\r\n').encode() +
                           (figure))

  conn.close()

setIndex()

def recvGET():
  while True:
   conn, addr = s.accept()
   data = conn.recv(2000)

   if 'GET' in data.decode():

        conn.sendall('Hello word'.encode())
        # dataParse = data.decode().split(' ')

        # if dataParse[1] == '/':
        #     conn.sendall(('HTTP/1.0 200 OK\r\n' +
        #               'Content-Type: text/html\r\n' +
        #               'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' +
        #               (homepage)).encode())
        # else:
        #     ext = dataParse[1].rpartition(".")[-1]
        #     f = open(dataParse[1][1:], 'r+b')
        #     figure = f.read()
        #     conn.sendall(('HTTP/1.0 200 OK\r\n' +
        #                   'Content-Type: image' + ext + '\r\n' +
        #                   'Content-Length: ' + str(len(figure)) + '\r\n\r\n').encode() +
        #                    (figure))

  conn.close()

recvGET()

s.close()

