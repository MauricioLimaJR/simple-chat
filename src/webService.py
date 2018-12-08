import socket # Networking support

class Server:
    """Class to a simple HTTP server"""

    data_decoded = ''
    content = ''

    def __init__(self, port = 8000):
        self.host = 'localhost'
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

        print ("Server was successfully up with the port: ", self.port)
        self._look_for_connections()

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

        return type

    def _look_for_connections(self):
        """Main loop to recieve the connections"""
        print ("Looking for some connection...\n")

        while True:
            self.socket.listen(25)
            conn, addr = self.socket.accept()

            print ("Got connection from: ",addr)

            data = conn.recv(2048)
            self.data_decoded = data.decode().split(' ')
            print (data)
            print ('olhaiiii: ', self.data_decoded[1])

            """Request Method"""
            request_method = self.data_decoded[0]
            print ("Resquest Method: ", request_method)

            if (request_method == 'GET') | (request_method == 'HEAD'):
                file_requested = self.data_decoded[1]
                """Check for arguments in the url. If it exists, just let it go"""
                file_requested = file_requested.split('?')[0]

                if (file_requested == '/'):
                    file_requested = 'index.html'
                elif (file_requested == '/teste'):
                    file_requested = 'index.html'

                file_requested = self.file_dir + file_requested
                self.response_content = ""

                """Loading the requested file"""
                try:
                    file = open(file_requested, 'r')
                    if (request_method == 'GET'):
                        self.response_content = file.read()
                    file.close()

                    response_headers = self._gen_headers(200)

                except Exception as e:
                    print('Could not found the file...')

                    response_headers = self._gen_headers(404)
                    if (request_method == 'GET'):
                        self.response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"

                server_response = response_headers

                if (request_method == 'GET'):
                    server_response += self.response_content

                conn.sendall(server_response.encode())

                print("Request was replied")
            else:
                print("Unknown HTTP request method: ", request_method)

        conn.close()

server = Server(8000)
server.start_server()