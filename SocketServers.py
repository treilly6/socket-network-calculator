import socket
from constants import HEADER_SIZE, SERVER_PORTS
import re
import sys
from eval_functions import eval_full_expression
from client import Client


worker_servers = [
  (socket.gethostname(), SERVER_PORTS['add'], 'addition'),
  (socket.gethostname(), SERVER_PORTS['sub'], 'subtraction'),
  (socket.gethostname(), SERVER_PORTS['mult'], 'multiplication'),
  (socket.gethostname(), SERVER_PORTS['div'], 'division'),
]


class SocketServer():
  def __init__(self, name):
    # self.s = socket.socket()

    self.name = name
    self.host = socket.gethostname()
    self.port = SERVER_PORTS[self.name.lower()]

    self.sock = None

    # self.print_details()
    self.run()

  def run(self):
    # create the socket
    self.sock = socket.socket()

    # bind the socket to the host and port
    self.sock.bind((self.host, self.port))

    print(f"started a {self.name} server at host {self.host} port {self.port}...")

    # allow 5 connections in queue
    self.sock.listen(5)

    while True:

      print(f"Waiting on a connection to {self.name} server")
      
      # this is blocking and will wait until a connection is established from a client (2)
      client_socket, client_addr = self.sock.accept()

      print(f"connection recieved from {client_addr} for {self.name} server")

      while True:
        print(f"In for loop of socket server {self.name}")
        msg_recieved = client_socket.recv(4096).decode('utf-8')

        if msg_recieved:
          
          print(f"MESSAGE HAS BEEN RECIEVED HERE IT IS -------> {msg_recieved}")
          if msg_recieved == 'Close':
            print(f"Closing {self.name} server")
            self.sock.close()
            return

          # strip all whitespace from the message
          msg_recieved = re.sub(r'\s+', '', msg_recieved)

          # split all the numbers and operators into items in a list
          # filter the list to remove empty strings
          elem_list = list(filter(None, re.split(r'(\+|\-|\*|/|\(|\))',msg_recieved)))

          # run the process method which is overridden by subclasses
          return_msg, close_server_socket = self.process(msg_recieved) # (3)

          print("AFTER THE PROCESS METHOD OF SOCKET SEVER")

          # Send a message back to the client socket
          client_socket.sendall(bytes(f"{return_msg}", "utf-8")) #(5)

          # close_server_socket variable is only True for the main server's process method
          # return values. This is so it will close itself after returning an answer to the client
          if close_server_socket:
            print(f"Closing the {self.name} server from the close_server_socket variable")
            self.sock.close()
            return
        else:
          break

      # print(f"Closing the connection made to {self.main} server")
      # client_socket.close()


  def print_details(self):
    print(f"Server Details:\n\thost : {self.host}\n\tport : {self.port}\n\tname : {self.name}")


class MainServer(SocketServer):
  def __init__(self):
    super().__init__(name = "Main")

  def test_network(self):
    host = socket.gethostname()

    full_msg = ''

    # try to ping each operation socket
    for server in worker_servers:
      print(f"trying to ping {server[2]}")

      # start a connection to one of the operation servers
      client = Client(server[0], server[1], "Echo msg")

      full_msg += client.return_msg
    
    return full_msg

  def process(self, msg_recieved, testing=False):
    print("Main Server Process Method") # (4)
    print(f"Message from the client : {msg_recieved}\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
      return self.test_network()
    
    print("NOT TESTING")
    answer = eval_full_expression(msg_recieved)

    for server in worker_servers:
      client = Client(server[0], server[1], "Close")

    print("Closing the main")

    return (answer, True)


        


class AddServer(SocketServer):
  def __init__(self):
    super().__init__(name = "Add")

  def process(self, msg_recieved):
    print(f"Adding {msg_recieved} = {eval(msg_recieved)}")
    return (str(eval(msg_recieved)), False)

  # def process(self, msg_recieved):
  #   print("Add Server Process Method")
  #   print(msg_recieved)
  #   return("Success Add\n")

class SubServer(SocketServer):
  def __init__(self):
    super().__init__(name = "Sub")

  def process(self, msg_recieved):
    print(f"Subtracting {msg_recieved} = {eval(msg_recieved)}")
    return (str(eval(msg_recieved)), False)

  # def process(self, msg_recieved):
  #   print("Sub Server Process Method")
  #   print(msg_recieved)  
    
  #   return("Success Subtraction\n")

class MultServer(SocketServer):
  def __init__(self):
    super().__init__(name = "Mult")

  # def process(self, msg_recieved):
  #   print("Mult Server Process Method")
  #   print(msg_recieved)  

  #   return("Success Multiplication\n")

  def process(self, msg_recieved):
    print(f"multiplying {msg_recieved} = {eval(msg_recieved)}")
    return (str(eval(msg_recieved)), False)

class DivServer(SocketServer):
  def __init__(self):
    super().__init__(name = "Div")

  def process(self, msg_recieved):
    print(f"Dividing {msg_recieved} = {eval(msg_recieved)}")
    return (str(eval(msg_recieved)), False)