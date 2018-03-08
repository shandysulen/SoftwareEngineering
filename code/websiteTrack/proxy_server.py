
import socket
import threading
import urllib.request
import signal
import sys

config = {
    "HOST" : "0.0.0.0",
    "PORT" : 10000,
    "MAX_REQUEST_LEN" : 1024,
    "CONNECTION_TIMEOUT" : 5
}

class ProxyServer:
    """ The HTTP proxy server class used to capture GET requests and responses """

    def __init__(self, config):
        # signal.signal(signal.SIGINT, self.stopServer) # Shutdown on Ctrl+C
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket, AF_INET = IPv4
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Re-use the socket
        self.socket.bind((config['HOST'], config['PORT'])) # bind the socket to a host IP address and a port
        self.socket.listen(10) # allow 1 unaccepted connections before refusing others
        self.__clients = []
        print("Server listening on port", config["PORT"] +  "...")

    def listenForClient(self):
        """ Listen for clients to connect with """
        while True:
            (client_socket, client_address) = self.socket.accept() # Establish the connection
            print("Client connection established with", client_address + ":" + client_socket + "...")
            self.addToClients(client_socket)
            self.printClients()
            d = threading.Thread(name=self._getClientName(client_address), target=self.proxy_thread, args=(client_socket, client_address))
            d.setDaemon(True)
            d.start()
        print("About to stop server")
        self.stopServer(0,0)

    def proxy_thread(self, conn, client_addr):
        """ A thread to handle a request from the browser """
        b_request = conn.recv(config['MAX_REQUEST_LEN']) # get the request from browser | Size limit: 1K
        print("Request:", b_request)
        str_request = str(b_request, 'utf-8')
        print("String Request:", str_request)
        first_line = str_request.split('\n')[0] # parse the first line and remove newline character
        print("First line:", first_line)
        url = first_line.split(' ')[1] # get url
        print("URL:", url)

        # find the webserver and port
        http_pos = url.find("://") # find pos of ://
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):] # get the rest of url

        port_pos = temp.find(":") # find the port pos (if any)

        # find end of web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if (port_pos==-1 or webserver_pos < port_pos):      # default port
            port = 80
            webserver = temp[:webserver_pos]
        else:                                               # specific port
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        print("Website:", webserver)
        print("Port:", port)

        try:
            # create a socket to connect to the web server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created to send requests to and receive responses from web server...")
            s.settimeout(config['CONNECTION_TIMEOUT'])
            s.connect((webserver, port))
            s.sendall(b_request) # send request to webserver

            while 1:
               data = s.recv(config['MAX_REQUEST_LEN'])          # receive data from web server
               print("Data received:", data)
               if (len(data) > 0):
                   conn.send(data)                               # send response back to client
               else:
                   print("PROXY CONNECTION GOT NO DATA FROM WEB SERVER")
                   break
            s.close() #Web server socket closed
            conn.close() #Client socket closed
        except socket.error as error_msg:
            print('ERROR: from shando',client_addr,error_msg)
            if s:
                s.close()
            if conn:
                conn.close()


    def _getClientName(self, cli_addr):
        """ Return the clientName """
        return cli_addr

    def addToClients(self, client_socket):
        self.__clients.append(client_socket)

    def printClients(self):
        for i in range(len(self.__clients)):
            print(i,":", self.__clients[i])


    def stopServer(self, signum, frame):
        """ Handle the exiting server by gracefully closing out """
        self.socket.close()
        sys.exit(0)


if __name__ == "__main__":
    server = ProxyServer(config)
    server.listenForClient()
