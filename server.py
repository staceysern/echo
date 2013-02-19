#! /usr/bin/env python

import sys, socket
import receiver 

PORT = 1060 

if len(sys.argv) > 2:
    print >> sys.stderr, "usage: {0} [interface]\n".format(sys.argv[0])
    sys.exit(1)

print "Blocking TCP Echo Server"

# Create a tcp socket to listen for connection requests
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# If the interface isn't specified, use the empty string for INADDR_ANY
interface = sys.argv[1] if len(sys.argv) == 2 else ''

# Bind the socket to the interface
try:
    server.bind((interface, PORT))
except socket.error as err:
    server.close()
    print >> sys.stderr, "Could not open socket: {0}".format(err)
    sys.exit(1)

# Set up the socket to listen for connection requests
server.listen(1)
print "Listening at {0}".format(str(server.getsockname()))

while True:
    # Wait for a connection request
    print "Waiting for a connection request"
    connection, client_addr = server.accept()
    print "Accepted connection from {0}".format(str(client_addr))
   
    # Each time a connection is established, create a receiver for the
    # socket
    rcvr = receiver.Receiver(connection)

    # Until the other end closes the socket, keep receiving messages
    # and echoing them back
    while rcvr.is_open():
        message = rcvr.recv_message()
        print "Received {0}".format(message),
        connection.sendall(message)

    # Close the socket
    connection.close()

