from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>hello!</body></html>"
                self.wfile.write(output)
                print(output)
                return 
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>hola! <a href='/hello'>Back to Hello</a></body></html>"
                self.wfile.write(output)
                print(output)
                return 
        except IOError:
            self.send_error(404,"file not found %s" % self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webServerHandler)
        print('web server running on %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C enterd, stopped web server')
        server.socket.close()



if __name__ == '__main__':
    main()