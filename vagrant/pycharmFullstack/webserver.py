
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import cgi #Common Gateway Interface

# need CRUD operations
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# make a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                '''
                the tomatoes business is how to deliver an actual website woohoo! Just need to add "tomato_script" into
                self.wfile.write(...) below

                '''
                #tomatoes = open("/vagrant/pycharmFullstack/pfresh_tomatoes.html")
                #tomato_script = tomatoes.read()
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='127.0.0.1:8080/restaurants/new'>Make a new restaurant</a>"
                for restaurant in restaurants:
                    output += "<p>"
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href=/restaurants/%s/edit>" % restaurant.id
                    output += "Edit</a>"
                    output += "</br>"
                    output += "<a href=/restaurants/%s/delete>" % restaurant.id
                    output += "Delete</a>"
                    output += "</br>"
                    output += "</p>"

                output += "</body></html>"
                self.wfile.write(output)
                print output

                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Make a restaurant!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestaurantName" type="text" placeholder = "New restaurant name"><input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output



            # This if statment and its companion in the do_POST method are straight up copy/pasted from instructor notes
            # I simply could not make mine work even though it looked very similar. I think the lack of organization in
            # my code was hiding some slight flaw making it difficult to spot.

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
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

                    return

            if self.path.endswith('/delete'):
                restaurant = session.query(Restaurant).filter_by(id = self.path.split("/")[2]).one()
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body"
                    output += '<h1>Delete %s?</h1>' % restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurant.id
                    output += "<input type= 'submit' value= 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)



            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>&#161Hola!  <a href='http://www.apple.com'>Back to Hello</" \
                          "a></body></html>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)













##POST handler##




    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(302)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0]
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return

            if self.path.endswith('/delete'):
                restaurantToDelete = session.query(Restaurant).filter_by(id = self.path.split("/")[2]).one()
                if restaurantToDelete:
                    session.delete(restaurantToDelete)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print " entered, stopping the web server..."
        server.socket.close()

if __name__=='__main__':
    main()
