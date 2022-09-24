#  coding: utf-8
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# TODO: 301 error and check the how secure...


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.decode("utf-8")
 
        if self.data[0:3] == 'GET':
            self.GET()
        else:
            self.METHODS_NOT_ALLOWED()
            return
        self.request.sendall(bytearray("OK", 'utf-8'))

    def GET(self): 
        # getting the path GET {path} /HTTP:1.1
        # checking the last char of the path if it is '/' or 'deep/' we need to push it to the home index.html
        if self.data.split(' ')[1][-1] == '/': 
            self.sendData('./www'+self.data.split(' ')[1]+'/index.html','text/html' ) 
        elif self.data.split(' ')[1][-3:] == 'css':
            self.sendData('./www'+self.data.split(' ')[1], 'text/css') 
        elif self.data.split(' ')[1][-4:] == 'html':
            self.sendData('./www'+self.data.split(' ')[1],'text/html')
        else:
            self.redirect(self.data.split(' ')[1]) 
            
    def redirect(self, url): 
        response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {url+'/'}\r\n"
        self.request.sendall(bytearray(response, 'utf-8'))

    def METHODS_NOT_ALLOWED(self):
        response = f"HTTP/1.1 405 Method Not Allowed\r\n∂"
        self.request.sendall(bytearray(response, 'utf-8'))

    def sendData(self, url, content_type):
        
        try:
            fp = open(url, 'r')
            data_to_send = fp.read()
            fp.close()
        except:
            response = f"HTTP/1.1 404 Not Found\r\n"
            self.request.sendall(bytearray(response,  'utf-8')) 
            return 
            
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(data_to_send)}\r\n\r\n{data_to_send}"
        self.request.sendall(bytearray(response, 'utf-8'))

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
