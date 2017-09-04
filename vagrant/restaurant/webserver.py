from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind = engine)
                session = DBSession()
                restaurants = session.query(Restaurant)
                output = ""
                output += "<html><body>"
                output += "<h1>Hello! Welcome to the restaurant list</h1>"
                output += "<a href='/new'>Add a new restaurant to the list</a>"
                output += "<ul>"
                for restaurant in restaurants:
                    output += "<li>%s</li>" % restaurant.name
                    output += "<a href='/%s/edit/'>Edit</a></br>" % restaurant.id
                    output += "<a href='/%s/delete/'>Delete</a>" % restaurant.id

                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new'>
								<h2>Please enter the name of the new restaurant</h2>
								<input name='new-restaurant-name' type='text'>
								<input type='submit' value='Submit'>
							</form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return   



            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<span>Hello /edit!</span>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return    

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                				<h2>What would you like me to say?</h2>
                				<input name="message" type="text" >
                				<input type="submit" value="Submit"> 
                			</form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/new'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new-restaurant-name')
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind = engine)
                session = DBSession()
                print messageContent
                print self.request.path
                print "hello spork"
                #restaurant = Restaurant(name = "%s" % self.request.name)





        	if self.path.endswith('/hello'):
	            self.send_response(301)
	            self.send_header('Content-type', 'text/html')
	            self.end_headers()
	            ctype, pdict = cgi.parse_header(
	                self.headers.getheader('content-type'))
	            if ctype == 'multipart/form-data':
	                fields = cgi.parse_multipart(self.rfile, pdict)
	                messagecontent = fields.get('message')
	            output = ""
	            output += "<html><body>"
	            output += " <h2> Okay, how about this: </h2>"
	            output += "<h1> %s </h1>" % messagecontent[0]
	            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
	            output += "</body></html>"
	            self.wfile.write(output)
	            print output
        except:
            pass

def main():
	try:
		#bloody everything is on 8080, I want to be able to run this while running other things
		port = 8079
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