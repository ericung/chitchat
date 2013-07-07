from socket import *
import sys
import select
import random
import string
from datetime import datetime

# user class
class User:
	session = "head"
	user = ""
	time = 0
	message = ""
	next = None
	
# usre pointers
userhead = User()

# bank of user data
def checkuser(usr,pwd):
	if (usr == 'Bob'):
		if (pwd == 'ini1'): 
			return 'success' 
		else: 
			return 'fail'
	if (usr == 'Tristan'):
		if (pwd == '31'): 
			return 'success' 
		else: 
			return 'fail'
	if (usr == 'admin'): 
		if (pwd == 'admin'): 
			return 'success'
		else: 
			return 'fail' 
	if (usr == 'Qwerty'): 
		if (pwd == 'asdf'): 
			return 'success' 
		else: 
			return 'fail' 
	if (usr == 'No More'): 
		if (pwd == 'Spaces'): 
			return 'success' 
		else: 
			return 'fail' 
	return 'fail'

# prints all the active users
def printlist():
	tmplist = userhead
	print "=== current list ==="
	while(tmplist.next != None):
		tmplist = tmplist.next
		print tmplist.session,tmplist.time
	print "===================="

# deletes a user
def deletesid( session ):
	tmplist = userhead
	prevnode = tmplist
	while(tmplist.next != None):
		tmplist = tmplist.next
		if (tmplist.session == session):
			prevnode.next = tmplist.next
			printlist()
			return 'success'
		prevnode = tmplist
	return 'fail'

# updates a user with session id specified
def update ( session ):
	tmplist = userhead
	curtime = datetime.now()
	while(tmplist.next != None):
		tmplist = tmplist.next
		if (tmplist.session == session):
			difference = datetime.now() - tmplist.time
			#if ((difference.seconds) > 300.0):
			if ((difference.seconds) > 300.0):
				timeoutuser = tmplist.user	
				deletesid( session )
				innerlist = userhead
				# print a timeout to all users
				while (innerlist.next != None):
					innerlist = innerlist.next
					innerlist.message = "{}\n{}:{} - Server > {} has timed out\n".format(innerlist.message, curtime.hour,curtime.minute, timeoutuser)
				return "timed out"
			if (tmplist.message != ""):
				msg = tmplist.message
				tmplist.message = ""
				return msg
	return "no new messages"

def masterupdate( time ):
	tmplist = userhead
	curtime = datetime.now()
	while (tmplist.next != None):
		tmplist = tmplist.next
		difference = curtime - tmplist.time
		if ((difference.seconds) > 300.0):
			innerlist = userhead
			while(innerlist.next != None):
				innerlist = innerlist.next
				innerlist.message = "{}\n{}:{} - Server > {} has timed out\n".format(innerlist.message, curtime.hour,curtime.minute, tmplist.user)
			print "timed out: ", tmplist.session
			deletesid( tmplist.session )
	return curtime

def login( usr, pwd ):
	# check user
	print checkuser(usr,pwd)
	if (checkuser(usr,pwd) == 'success'):
		chars = string.ascii_uppercase + string.digits
		rand = ''.join(random.choice(chars) for x in range(10))
		tmplist = userhead
		curtime = datetime.now()

		# print to all users
		while(tmplist.next != None):
			tmplist = tmplist.next
			tmplist.message = "{}\n{}:{} - Server > {} has logged in\n".format(tmplist.message, curtime.hour,curtime.minute, usr)
			print "logging in: ", tmplist.session, tmplist.time
		
		# make a new user
		newuser = User()
		newuser.session = rand
		newuser.user = usr
		newuser.time = datetime.now()
		newuser.message = "{}\n{}:{} - Server > Welcome\n".format(tmplist.message, curtime.hour,curtime.minute)
		print rand, newuser.time 
		tmplist.next = newuser
		return rand
	else:
		return 'fail'

# logging out
def logout( session ):
	print "logging out: ", session
	curtime = datetime.now()

	# find the user logging out
	loglist = userhead
	loguser = ''
	while(loglist.next != None):
		loglist =loglist.next
		if (loglist.session == session):
			loguser = loglist.user

	# print
	tmplist = userhead
	while(tmplist.next != None):
		tmplist = tmplist.next
		tmplist.message = "{}\n{}:{} - Server > {} has logged out\n".format(tmplist.message, curtime.hour,curtime.minute, loguser)
	# delete user
	return deletesid( session )

def sendmsg( sid, msg ):
	print "sending message: ", msg
	tmplist = userhead
	fromsid = userhead
	curtime = datetime.now()
	
	# find user
	while(tmplist.next != None):
		tmplist = tmplist.next
		if (tmplist.session == sid):
			fromsid = tmplist
	if (fromsid == userhead):
		return
	fromsid.time = datetime.now()

	# updating server
	tmplist = userhead
	while (tmplist.next != None):
		tmplist = tmplist.next
		tmplist.message = "{}\n{}:{} - {} > {}\n".format(tmplist.message, curtime.hour,curtime.minute, fromsid.user,msg)
		print "updating message: ", tmplist.session, tmplist.message 

def main():
	# set up server
	argdom = sys.argv[1]
	arghost = sys.argv[2]
	address = ('{}'.format(argdom),int(arghost))
	server_socket = socket(AF_INET, SOCK_DGRAM)
	server_socket.bind(address)
	mastertime = datetime.now()
	print gethostname()
	print gethostbyaddr('cgi.cselabs')

	# have server loop
	while(1):
		recv_data, addr = server_socket.recvfrom(2048)
		recieve = recv_data.split("@@@@")
		if (recieve[0] != "update"):
			print "Listening"
		if (recieve[0] == "login"):
			sid = login( recieve[1],recieve[2] )
			server_socket.sendto(sid, addr)
		if (recieve[0] == "logout"):
			retval = logout( recieve[1] )
			server_socket.sendto( retval, addr )
		if (recieve[0] == "send"):
			sendmsg( recieve[1],recieve[2] )
		if (recieve[0] == "update"):
			retval = update( recieve[1] )
			server_socket.sendto( retval, addr )
		mastertime = masterupdate( mastertime )

	server_socket.close()

main()

