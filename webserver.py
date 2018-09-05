import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print(self.path)
            if self.path.endswith("/restaurants"):
                print('restaurant')
                resturants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = "<html>"
                output += "<body>"
                output += "<a href='/restaurants/new'>Create a new restaurant </a>" 
                output += "<div>"
                for resturant in resturants:
                    output += "<div id='%s'>" % resturant.name
                    output += "<h3> " + resturant.name + "</h3>"
                    output += "<div>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % resturant.id
                    output += "<a href='/restaurants/%s/delete'>Delete </a>" % resturant.id
                    output += "</div>"
                    output += "</div>"
                    output += "<br>"
                output += "</div>"
                output += "</body>"
                output +="</html>"
                self.wfile.write(output)
                print(output)
                return 
            if self.path == '/restaurants/new':
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = "<html>"
                output += "<body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='restaurant-name' type='text' required>"
                output += "<button name='create' type='submit' value='Submit'>Create</button>"
                output += "</form>"
                output += "</body>"
                output += "</html>"
                self.wfile.write(output)
                print(output)
                return
            
            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = "<html>"
                output += "<body>"
                output += "<h1>Rename a Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += "<input name='restaurant-name' type='text' required>"
                output += "<button name='create' type='submit' value='Submit'>Submit</button>"
                output += "</form>"
                output += "</body>"
                output += "</html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = "<html>"
                output += "<body>"
                output += "<h1>Delete a Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += "<button name='create' type='submit' value='Submit'>Delete</button>"
                output += "</form>"
                output += "<a href='/restaurants'>Back to previous page</a>"
                output += "</body>"
                output += "</html>"
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404,"file not found %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith('/new'):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('restaurant-name')
                    newResturant = Restaurant(name=name[0])
                    session.add(newResturant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                    return
            if self.path.endswith('/edit'):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    tokens = self.path.split('/')
                    print(tokens)
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('restaurant-name')[0]
                    print(tokens[2])
                    restaurant = session.query(Restaurant).filter_by(id=int(tokens[2])).first()
                    if(restaurant != []):
                        restaurant.name = name
                        session.add(restaurant)
                        session.commit()
                    self.send_response(301)
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                    return
            if self.path.endswith('/delete'):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    tokens = self.path.split('/')
                    print(tokens)
                    print(tokens[2])
                    restaurant = session.query(Restaurant).filter_by(id=int(tokens[2])).first()
                    if(restaurant != []):
                        session.delete(restaurant)
                        session.commit()
                    self.send_response(301)
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                    return

        except:
            pass
        

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