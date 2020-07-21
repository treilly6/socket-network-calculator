from SocketServers import AddServer, MainServer, SubServer, MultServer, DivServer
import threading

class CalcNetwork:
  def __init__(self):
    # init a bool value which tracks whether all network resources are created
    self.full_network_started = False

    # start each resource of the network in its own thread
    main_server = threading.Thread(target = MainServer)
    add_server = threading.Thread(target = AddServer)
    sub_server = threading.Thread(target = SubServer)
    mult_server = threading.Thread(target = MultServer)
    div_server = threading.Thread(target = DivServer)

    main_server.start()
    add_server.start()
    sub_server.start()
    mult_server.start()
    div_server.start()

    self.full_network_started = True

    print("All the threads are completed")