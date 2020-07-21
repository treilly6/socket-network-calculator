import socket
from constants import HEADER_SIZE, SERVER_PORTS
from time import sleep
import sys
from client import Client
from CalcNetwork import CalcNetwork

  
if __name__ == "__main__":
  print("Enter an expression to be evaluated : ")
  math_exp = input()

  print(math_exp)

  # have some kind of input validation here
  # 
  # 

  # have some kind of validation here for the expression

  print("Starting Network ...")

  # start the network
  # starts the main server and the operator servers (+,-,/,*)
  network = CalcNetwork()

  # wait for the full network to be created
  # using this because the servers are started in threads
  # and e=want to make sure all are started before continuing
  while not network.full_network_started:
    sleep(1)

  print("Calculator Network Running")

  # get hostname
  host = socket.gethostname()

  # use the port of the main server
  port = SERVER_PORTS['main']

  # start a client connection to the main server port and pass the math_expression
  client = Client(host = host, port = port, message = math_exp)

  print(f"Expression ---> {math_exp}")
  print(f"Answer -------> {client.return_msg}")
