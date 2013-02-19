#! /usr/bin/env python

import sys, socket
import receiver 

PORT = 1060 

if len(sys.argv) != 2:
    print >> sys.stderr, "usage: {0} host\n".format(sys.argv[0])
    sys.exit(1)

print "TCP Echo Client"

host = sys.argv[1]

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

# Create a receiver object for the socket and as long as the other side
# hasn't closed the socket, read input from the user until they enter a
# period, send it to the server, and try to receive the echo
rcvr = receiver.Receiver(tcp_socket)
while rcvr.is_open():
    message = raw_input()
    if message != ".":
        tcp_socket.sendall(message+"\n")

        # Get the echo
        echo = rcvr.recv_message() 
        print echo,
    else: 
        tcp_socket.close()
        sys.exit(1)

