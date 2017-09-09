from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant)
                output = ""
                output += "<html><body>"
                output += "<h1>Hello! Welcome to the restaurant list</h1>"
                output += "<a href='/restaurants/new'>Add a new restaurant to the list</a>"
                output += "<ul>"
                for restaurant in restaurants:
                    output += "<li>%s</li>" % restaurant.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a></br>" % restaurant.id
                    output += "<a href='/restaurants/%s/update'>Update</a></br>" % restaurant.id
                    output += "<a href='/%s/delete'>Delete</a>" % restaurant.id

                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
								<h2>Please enter the name of the new restaurant</h2>
								<input name='newRestaurantName' type='text'>
								<input type='submit' value='Submit'>
							</form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return   

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
            if self.path.endswith("/update"):
                restaurant_id = int(self.path.split("/")[2])     
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()         
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                if restaurant:
                    output = "<html><body>"
                    output += "<h1>Hello!</h1>"
                    output += '''<span>Hello /edit!</span>'''
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/update'>
                                    <input name='restaurantName' value='%s' type='text'>
                                    <input name='restaurantId' value='%i' type='hidden'>
                                    <input type='submit' value='Submit'>
                                </form>''' % (restaurant.name, restaurant.id)
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output

                    
                return 

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()


            if self.path.endswith("/update"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('newRestaurantName')
                    restaurantId = fields.get('restaurantId')
                
                    restaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()

                    if restaurantQuery != [] :
                        restaurantQuery.name = restaurantName
                        session.add(restaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()


            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()


            

                #return


        except:
            self.send_error(404, 'Unable to add new restaurant: %s' % self.path)

def main():
	try:
		#bloody everything is on 8080, I want to be able to run this while running other things
		port = 8080
		# class HTTPServer.HTTPServer(server_address, RequestHandlerClass)
		# This class builds on the TCPServer class by storing the server address 
		# as instance variablesnamed server_name and server_port. The server is 
		# accessible by the handler, typically through the handler/'s server instance variable
		server = HTTPServer(('', port), webserverHandler)
		print "Web server running on port %s" % port

		server.serve_forever()

	#this is a built-in exception in python triggerd by user hitting ctrl-c on their keyboard
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()


if __name__ == '__main__':
	main()