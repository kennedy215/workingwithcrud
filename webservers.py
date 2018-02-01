from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#import CRUD Operations from Lesson Content
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Create Session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #output
                output += "<html><body>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br></br></br>"
                    output += "<a href =' #'>Edit</a>"
                    output += "</br>"
                    output += "<a href = ' #'>Delete</a>"
                    output += "</br>"



                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def main():
    try:
        port = 8082
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
