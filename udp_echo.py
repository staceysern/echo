import sys, socket

PORT = 1060
MAX = 65535

if 2 <= len(sys.argv) <=3 and sys.argv[1] == 'server':
    # Server
    print "UDP Echo Server"

    # Create a udp socket and bind it to an address
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # If the interface isn't specified, use the empty string for INADDR_ANY
    interface = sys.argv[2] if len(sys.argv) == 3 else ''
    udp_socket.bind((interface, PORT))
    
    # Look for messages and echo them back 
    while True:
        msg, addr = udp_socket.recvfrom(MAX) 
        print "Received '" + msg + "' from " + str(addr)
        udp_socket.sendto(msg, addr)

elif len(sys.argv) == 4 and sys.argv[1] == 'client':
    # Client
    print "UDP Echo Client"

    host = sys.argv[2]
    message = sys.argv[3]
    
    # Create a udp socket and connect to the host
    # By connecting to the host, this socket will only accept messages from 
    # the specified address
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.connect((host, PORT))

    # Send the message
    udp_socket.send(message)

    # Get the echo
    echo = udp_socket.recv(MAX)
    print "Received '" + echo + "'"
    
else:
    sys.stderr.write("usage: {0} server [interface]\n".format(sys.argv[0]))
    sys.stderr.write("   or: {0} client host message\n".format(sys.argv[0]))
