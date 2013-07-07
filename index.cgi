#!/usr/bin/python 

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import sys
from socket import *
import select

client_socket = socket(AF_INET, SOCK_DGRAM)
print "Content-Type: text/html;\n\n"

# generates the basic form set to logging in at default
def generateform():
	f = open('chitchat.html','r')
	print f.read()
	f.close()

# send logging in request to server
def generatelogin( username,password,domain,port ):
	address = ( domain,int(port) )
	data = "login@@@@{}@@@@{}".format( username,password )
	client_socket.sendto( data,address )
	sessionid, address = client_socket.recvfrom( 2048 )
	print sessionid

# send logging out request to server
def generatelogout( sid, domain, port ):
	data = "logout@@@@{}".format( sid )
	address = ( domain,int(port) )
	client_socket.sendto( data,address )
	retval, address = client_socket.recvfrom( 2048 )
	print retval

# send a message request to servers
def generatesend( sid, domain, port, message ):
	# send
	data = "send@@@@{}@@@@{}".format( sid, message )
	address = ( domain,int(port) )
	client_socket.sendto( data,address )

# send an update request to the servers
def generateupdate( sid, domain, port ):
	data = "update@@@@{}".format( sid )
	address = ( domain,int(port) )
	client_socket.sendto( data,address )
	message, address = client_socket.recvfrom( 2048 )
	print message
		
# main procedure
def main():
	form = cgi.FieldStorage()

	if (form.has_key("action")):
		if (form["action"].value == 'login'):
			generatelogin(form["username"].value,form["password"].value,form["domain"].value,form["port"].value)
		elif (form["action"].value == 'logout'):
			generatelogout( form["session"].value, form["domain"].value, form["port"].value )
		elif (form["action"].value == 'send'):
			generatesend( form["session"].value, form["domain"].value, form["port"].value, form["message"].value )
		elif (form["action"].value == 'update'):
			generateupdate( form["session"].value, form["domain"].value, form["port"].value )
	else:
		generateform()


main()
