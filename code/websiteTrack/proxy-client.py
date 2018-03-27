import requests
import time

class ProxyClient:
    '''
    The proxy client connects to the web server that runs Kitten's forward web proxy.
    The user chooses which websites he or she would like to track. The ProxyClient object
    receives the amount of times these websites are accessed, which is saved in a .csv file.

    self.host: The web server's IP address that runs the web proxy
    self.port: The web server's port that serves the log information
    self.website: A space delimited string that holds the websites the user wishes to track
    '''

    def __init__(self, host, port):
        self.host = host
        self.port = port
        # Set proxy info on browsers automatically

    def getWebsites(self):
        self.websites = input("Please enter the websites that you would like to track the usage of: ")

    def getLog(self):
        # Disable proxy info on web browsers
        # proxies = {
        #     'http':'http://167.99.61.206:3128',
        #     'https':'http://167.99.61.206:3128',
        # }
        try:
            response = requests.post('http://' + self.host + ':' + str(self.port), data=self.websites)
        except ConnectionError:
            print("Unable to connect with Kitten server...")

        with open('website_log.csv', 'a') as log:
            log.write(response.text)

if __name__ == '__main__':
    client = ProxyClient('167.99.61.206', 8080)
    client.getWebsites()
    print("Tracking website usage...")
    time.sleep(3) # have proxy run for 20 seconds
    client.getLog()
    print("Logging information added to website_log.csv...")
