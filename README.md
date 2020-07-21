# socket-network-calculator
A network of servers connected via python sockets. A calculator cluster composed of a main server which parses a mathematical expression and sends pieces of the expression to worker nodes (each worker node represents one math operator among multiplication, division, addition, and subtraction). The main server receives the math expression from a client via a socket connection

Run "python run_server.py" from the command line to start the calculator
