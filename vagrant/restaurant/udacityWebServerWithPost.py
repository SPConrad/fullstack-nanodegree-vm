def do_POST(self):
    try:
        self.send_response(301)        
        self.send_headers('Content-type', 'text/html')
        self.end_headers()
        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
        output = ""
        output += "<html><body>"
        output += "<h2>Okay, how about this: </h2>"
        output += "<h1> %s </h1>" % messagecontent[0]
        output += "<form method='POST' enctype='multipart/form-data' action ='/hello><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
        output += "</body><html>"
        self.wfile.write(output)
        print output
    except: 
        pass