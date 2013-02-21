#! /usr/bin/env python
"""Usage: server.py [interface]"""

import sys, socket, select

PORT = 1060 
MAX = 1024

if len(sys.argv) > 2:
    print >> sys.stderr, "usage: {0} [interface]\n".format(sys.argv[0])
    sys.exit(1)

# If the interface isn't specified, use the empty string for INADDR_ANY
interface = sys.argv[1] if len(sys.argv) == 2 else ''

print "Non-Blocking TCP Echo Server"

# Create a non-blocking tcp socket to listen for connection requests
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)

# Bind the socket to the interface
try:
    server.bind((interface, PORT))
except socket.error as err:
    server.close()
    print >> sys.stderr, "Could not open socket: {0}".format(err)
    sys.exit(1)

# Set up the socket to listen for connection requests
server.listen(5)
print "Listening at {0}".format(str(server.getsockname()))

# Keep track of sockets used for reading and writing
inputs = [server]  
outputs = []       

# Messages maps output sockets to a list of messages waiting to be sent
messages = {}

while inputs:
    # See which sockets have generated events
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle sockets which are ready for reading 
    for s in readable:
        if s is server:
            # Accept connection requests
            connection, client_addr = server.accept()
            print "Accepted connection from {0}".format(str(client_addr))

            connection.setblocking(0)
            inputs.append(connection)

        else:
            # Get the data from the socket 
            data = s.recv(MAX)
            if data:
                print "Received {0} from {1}".format(data,s.getpeername())
                 
                if s not in outputs:
                    outputs.append(s)
                    messages[s] = []

                messages[s].append(data)
            else:
                # The empty string implies that the connection has been closed
                # so remove references to the socket and close it
                print "Closing {0} upon reading no data".format(s.getpeername())
                if s in outputs:
                    outputs.remove(s)
                    del messages[s]
                inputs.remove(s)
                s.close()

    # Handle sockets which are ready for writing 
    for s in writable:
        # Make sure that the socket hasn't closed since its writable status was
        # checked
        if s in outputs:
            # Check whether there is more data to write to the socket
            if messages[s] == []:
                # If there is nothing more to write to this socket, remove it 
                # from the outputs list and remove its list of messages
                outputs.remove(s)
                del messages[s]
            else:
                # Send the first message in the message queue 
                n = s.send(messages[s][0])

                # Check whether the entire message was able to be sent
                if n == len(messages[s][0]):
                    print "Sent {0} to {1}".format(messages[s][0], 
                                                   s.getpeername())

                    # Remove the message from the queue
                    messages[s] = messages[s][1:]
                else:
                    print "Sent {0} to {1}".format(messages[s][0][:n], 
                                                   s.getpeername())

                    # Remove the bytes that were sent from the first message in
                    # the queue
                    messages[s][0] = messages[s][0][n:]

    # Handle sockets which have an exceptional condition 
    for s in exceptional:
        print "Closing {0} upon exceptional condition".format(s.getpeername())

        # Remove references to the socket and close it 
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
            del messages[s]
        s.close()

