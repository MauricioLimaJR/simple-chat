import socket # Networking support
import threading
import sys
import json

class Server:
    """Class to a simple HTTP server"""
    
    data_decoded = ''
    content = ''
    messages = []

    def __init__(self, port = 8000):
        self.host = ''
        self.port = port
        self.file_dir = '../'

    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print ("Starting server on ",self.host,":",self.port,"\n")
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print ("Warning: could not to connect by port ", self.port)
            self.shutdown_server()

        self.socket.listen(5)

        looking_for = threading.Thread(target=self._look_for_connections)
        looking_for.daemon = True
        looking_for.start()

        looking_for_two = threading.Thread(target=self._look_for_connections)
        looking_for_two.daemon = True
        looking_for_two.start()

        while True:
            print('Para fechar o servidor digite: close')
            msg = input('->')
            if msg == 'close' or msg == 'CLOSE':
                self.socket.close()
                sys.exit()
            else:
                pass

        print ("Server was successfully up with the port: ", self.port)

    def shutdown_server(self):
        try:
            print("bye-bye")
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print ("Ops! We can't to close it.")

    def _gen_headers(self, code):
        header = ''
        if (code == 200):
            header = ('HTTP/1.0 200 OK\r\n' +
                    'Access-Control-Allow-Origin: *' + '\r\n' +
                    'Access-Control-Allow-Headers: Content-Type,Authorization' + '\r\n' +
                    'Access-Control-Allow-Methods: GET,PUT,POST,DELETE,OPTIONS' + '\r\n' +
                    'Content-Type: ' + self._get_content_type() + '\r\n' +
                    'Content-Length: ' + str(len(self.response_content)) + '\r\n\r\n'
                    )
        elif(code == 404):
            header = 'HTTP/1.1 404 Not Found\n'

        return header

    def _get_content_type(self):
        type = ''
        string = self.data_decoded[1]

        if ('js' in string) | ('JS' in string):
            type = 'text/javascript'
        elif ('css' in string) | ('CSS' in string):
            type = 'text/css'
        elif ('html' in string) | ('HTML' in string):
            type = 'text/html'
        elif ('ico' in string) | ('ICO' in string):
            type = 'ico'

        return type

    def _look_for_connections(self):
        """Main loop to recieve the connections"""
        print ("Looking for some connection...\n")

        while True:
            self.socket.listen(5)
            conn, addr = self.socket.accept()

            print ("Got connection from: ",addr)

            data = conn.recv(2048)
            if not data: break
            self.data_decoded = data.decode().split(' ')
            print ('Data resquest :', data)
            print ('Requested object: ', self.data_decoded[1])

            """Request Method"""
            request_method = self.data_decoded[0]
            print ("Resquest Method: ", request_method)

            if (request_method == 'GET') | (request_method == 'HEAD'):
                file_requested = self.data_decoded[1]
                # Check for arguments in the url. If it exists, just let it go
                file_requested = file_requested.split('?')[0]
                self.response_content = ""

                if ('ico' in file_requested):
                    """Request for some image"""
                    file_requested = self.file_dir + file_requested
                    try:
                        file = open(file_requested, 'r+b')
                        self.response_content = file.read()
                        file.close()

                        response_headers = self._gen_headers(200)
                        print ('Image is ok.')
                    except Exception as e:
                        print('Could not found requested image...')

                        if (request_method == 'GET'):
                            self.response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
                        response_headers = self._gen_headers(404)

                    server_response = response_headers
                elif ('wav' in file_requested):
                    file_requested = self.file_dir + file_requested
                    try:
                        file = open(file_requested, 'r+b')
                        self.response_content = file.read()
                        file.close()

                        response_headers = self._gen_headers(200)
                        print ('Sound is ok.')
                    except Exception as e:
                        print('Could not found requested song...')

                        if (request_method == 'GET'):
                            self.response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
                        response_headers = self._gen_headers(404)

                    server_response = response_headers
                else:
                    """Request for some text file"""

                    # Requesting for test
                    if file_requested == '/teste':
                        self.response_content = 'Funcionou papai....'
                        response_headers = self._gen_headers(200)
                    # Resquest for send a message
                    elif file_requested == '/send_message':
                        message = self.data_decoded[1].split('?')[1]
                        message = message.split('=')[1]

                        message = message.replace('%20', ' ')
                        message = message.replace('%3A', ':')
                        message = message.replace('%3F', '?')

                        self.messages.append(message)

                        self.response_content = 'ok'
                        response_headers = self._gen_headers(200)
                    # Request for messages
                    elif file_requested == '/get_messages':
                        if len(self.messages) == 0:
                            messages = ""
                        else:
                            messages = json.dumps(self.messages)

                        self.response_content = messages
                        response_headers = self._gen_headers(200)
                    # Request for some file
                    else:
                        if file_requested == '/':
                            file_requested = 'index.html'

                        file_requested = self.file_dir + file_requested

                        """Loading the requested file"""
                        try:
                            file = open(file_requested, 'r')
                            if request_method == 'GET':
                                self.response_content = file.read()
                            file.close()

                            response_headers = self._gen_headers(200)

                        except Exception as e:
                            print('Could not found the file...')

                            if request_method == 'GET':
                                self.response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
                            response_headers = self._gen_headers(404)

                    server_response = response_headers

                if ('ico' not in file_requested) and ('wav' not in file_requested):
                    if request_method == 'GET':
                        server_response += self.response_content
                    conn.sendall(server_response.encode())
                else:
                    if request_method == 'GET':
                        server_response = server_response.encode()
                    conn.sendall(server_response+self.response_content)

                print("Request was replied\n")
            else:
                print("Unknown HTTP request method: ", request_method)

        conn.close()

server = Server(8000)
server.start_server()