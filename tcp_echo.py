import sys, socket

PORT = 1060 
MAX = 65535

# This program implements a blocking TCP Echo Server and its companion TCP Echo
# Client.  The server accepts requests from clients to establish a connection
# over which it receives a variable length message.  Then it echoes the message
# back to the client. The server is capable of communicating with only one
# client at a time. 

# recvall returns a string that represents a complete message that is sent over
# the specified socket. The end of the message is determined when the socket
# recv function returns an empty string which indicates that the client has
# closed the socket at least for writing. 
def recvall(socket):
    data = ''
    more = socket.recv(MAX) 
    while more <> '':
        data += more
        more = socket.recv(MAX)
    return data

if 2 <= len(sys.argv) <=3 and sys.argv[1] == 'server':
    # Server
    print "Blocking TCP Echo Server"

    # Create a tcp socket to listen for connection requests
    listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # If the interface isn't specified, use the empty string for INADDR_ANY
    interface = sys.argv[2] if len(sys.argv) == 3 else ''

    # Bind the socket to the interface
    try:
        listen.bind((interface, PORT))
    except socket.error as err:
        listen.close()
        sys.stderr.write("Could not open socket: {0}\n".format(err))
        sys.exit(1)
    
    # Set up the socket to listen for connection requests
    listen.listen(1)
    print "Listening at " + str(listen.getsockname())

    # Look for messages and echo them back 
    while True:
        connection, peer_addr = listen.accept()
        print "Accepted connection from " + str(peer_addr)
        
        message = recvall(connection)
        if message <> '':
            print "Received '" + message + "'"
            connection.sendall(message)
        connection.close()

elif len(sys.argv) == 4 and sys.argv[1] == 'client':
    # Client
    print "TCP Echo Client"

    host = sys.argv[2]
    message = sys.argv[3]
    
    # Create a tcp socket and connect to the host
    # By connecting to the host, this socket will only accept messages from 
    # the specified address
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_socket.connect((host, PORT))
    except socket.error as err :
        tcp_socket.close()
        sys.stderr.write("Connection failed: {0}\n".format(err))
        sys.exit(1)

    # Send the message and shutdown the socket for writing so the server will
    # be able to detect the end of the message
    tcp_socket.sendall(message)
    tcp_socket.shutdown(socket.SHUT_WR)

    # Get the echo
    echo = recvall(tcp_socket) 
    print "Received '" + echo + "'"
    tcp_socket.close()
    
else:
    sys.stderr.write("usage: {0} server [interface]\n".format(sys.argv[0]))
    sys.stderr.write("   or: {0} client host message\n".format(sys.argv[0]))
