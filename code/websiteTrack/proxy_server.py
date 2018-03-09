
import socket
import sys

config = {
    "HOST" : '',
    "PORT" : 10000,
    "MAX_REQUEST_LEN" : 4096,
    "CONNECTION_TIMEOUT" : 5
}

class ProxyServer:
    """ The HTTP proxy server class used to capture GET requests and responses """

    def __init__(self, config):
        try:
            # signal.signal(signal.SIGINT, self.stopServer) # Shutdown on Ctrl+C
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket, AF_INET = IPv4
            self.s.bind((config['HOST'], config['PORT'])) # bind the socket to a host IP address and a port
            self.s.listen(10) # allow 10 unaccepted connections before refusing others
            print("Server listening on port", str(config["PORT"]) + "...")
        except Exception as e:
            print("Unable to initialize socket...")
            sys.exit() # Successful termination


    def listenForClient(self):
        """ Listen for clients to connect with """
        while True:

            # Establish connection
            (conn, address) = self.s.accept()
            print("Client connection established with", str(conn))

            # Get request from browser | Size limit: 1K
            b_request = conn.recv(config['MAX_REQUEST_LEN'])

            if (len(b_request) == 0):
                continue

            print("Request:", b_request)
            str_request = str(b_request, 'utf-8')
            print("String Request:", str_request)
            first_line = str_request.split('\n')[0] # parse the first line and remove newline character
            print("First line:", first_line)
            url = first_line.split(' ')[1] # get url
            print("URL:", url)

            # Find domain and port
            if url.find("http://www.") != -1 and (url.find(":80") != -1 or url.find(":443") != -1):
                domain = url[url.find("http://www.") + 11 : url.find(":")]
                port = int(url[url.find(":") + 1 : ])
            elif url.find("www.") != -1 and (url.find(":80") != -1 or url.find(":443") != -1):
                domain = url[url.find("www.") + 4 : url.find(":")]
                port = int(url[url.find(":") + 1 : ])
            elif url.find("http://") != -1 and (url.find(":80") != -1 or url.find(":443") != -1):
                domain = url[url.find("http://") + 7 : url.find(":")]
                port = int(url[url.find(":") + 1 : ])
            elif url.find("www.") != -1 and url.find(":80") == -1 and url.find(":443") == -1:
                domain = url[url.find("www.") + 4 : ]
                port = 80
            elif url.find("http://") == -1 and url.find("www.") == -1 and url.find(":80") == -1 and url.find(":443") == -1:
                domain = url[ : url.find(":")]
                port = int(url[url.find(":") + 1 : ])
            else:
                domain = url
                port = 80

            print("Domain:", domain)
            print("Port:", port)

            try:
                # Create web server socket for proxy to connect to web server
                webserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Socket created to send requests to and receive responses from web server...")
                # webserver_socket.settimeout(config['CONNECTION_TIMEOUT']) POSSIBLE PROBLEM?
                webserver_socket.connect(("www." + domain, port)) # connect to webserver
                print("Connected to remote server...")
                request = "GET " + "http://www." + domain + " HTTP/1.1\r\n\r\n"
                webserver_socket.send(str.encode(request)) # send request to webserver
                print(str.encode(request))
                print("Successfully sent request...")

                # Receive data from web server
                while True:
                    data = webserver_socket.recv(config['MAX_REQUEST_LEN'])
                    data_string = str(data, 'utf-8')
                    print("Data received:", data_string)

                    # Send response back to client
                    if (len(data) > 0):
                        conn.send(data)
                    else:
                        print("PROXY CONNECTION GOT NO DATA FROM WEB SERVER")
                        break;

                # Close socket connections
                webserver_socket.close()
                conn.close()

            except socket.error as error_msg:
                # Print error and close socket connections
                print("shando", error_msg)
                webserver_socket.close()
                conn.close()

if __name__ == "__main__":

    try:
        server = ProxyServer(config)
        server.listenForClient()
    except KeyboardInterrupt:
        print("Exiting application...")
        sys.exit(0) # Successful termination
