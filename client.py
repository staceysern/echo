#! /usr/bin/env python
"""Usage: client.py host"""

import sys, socket

PORT = 1060 

if len(sys.argv) != 2:
    print >> sys.stderr, "usage: {0} host\n".format(sys.argv[0])
    sys.exit(1)

host = sys.argv[1]

print "TCP Echo Client"

# Create a tcp socket 
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# By connecting to the host, this socket will only accept messages from 
# the specified address
try:
    tcp_socket.connect((host, PORT))
except socket.error as err:
    tcp_socket.close()
    print >> sys.stderr, "Connection failed: {0}\n".format(err)
    sys.exit(1)

while True:
    message = raw_input()
    if message == ".":
        # Close the program
        tcp_socket.close()
        sys.exit(1)
    else:
        # Send the message
        tcp_socket.sendall(message)

        # Get the echo
        bytes_expected = len(message)
        bytes_received = 0
        echo = []

        # Ask the socket for incoming data until the entire message has been 
        # received based on the length of the message
        while bytes_received < bytes_expected:
            msg_chunk = tcp_socket.recv(bytes_expected - bytes_received)
            if msg_chunk:
                echo.append(msg_chunk)
                bytes_received += len(msg_chunk)
            else:
                # Socket unexpectedly closed before the echo was fully received
                print "Socket closed before echo was received"
                tcp_socket.close()
                sys.exit(1)
        print "".join(echo)


