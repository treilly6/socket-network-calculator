import socket

class Client:
  def __init__(self, host, port, message):

    host = socket.gethostname() if host == None else host

    self.sock = socket.socket()

    self.return_msg = None

    # connect to the host and the port of the main server
    # since I'm running this on local machine I can use the
    # gethostname() method above however if this was deployed on
    # a server you would want the host to be the hostname/ip address
    # of the server
    self.sock.connect((host,port)) # makes a connection to the main server (1)

    # send the expression to the main server
    self.sock.sendall(bytes(message, "utf-8"))

    # message returned from the server
    server_msg = self.sock.recv(4096).decode('utf-8')

    print(f"Finished Message Returned To Client\n{server_msg}")

    # set message returned from the server to the instance
    self.return_msg = server_msg