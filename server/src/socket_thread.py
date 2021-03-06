import threading
from . import game_system as gs


class SocketThread(threading.Thread):
  def __init__(self, s, args):
    super().__init__()
    self.socket = s
    self.verbose = args.verbose

  def run(self):
    while True:
      data = self.socket.recv_obj()

      if not data:
        gs.remove_player(self.socket)
        return
      if not data.get("command"):
        break

      if self.verbose:
        print("received data : {}".format(data))
      
      command = data["command"]

      if command == "update":
        self.update(data)
      elif command == "create":
        self.create(data)
      elif command == "join":
        self.join(data)
      elif command == "list":
        self.list_games()

    self.socket.close()

  def update(self, data):
    if not data.get("status"):
      self.socket.send_error("A status must be specified")
    
    else:
      gs.update_status(self.socket, data["status"])

  def create(self, data):
    if not data.get("host"):
      self.socket.send_error("A host must be specified")
    elif not data.get("nb_players"):
      self.socket.send_error("The numbers of players is required")
    elif not data.get("mission"):
      self.socket.send_error("A mission file is required")

    else:
      if self.verbose:
        print("Creating new game hosted by '{}'".format(data["host"]))
      gs.new_game(self.socket, data["host"], data["nb_players"], data["mission"])

  def join(self, data):
    if not data.get("host"):
      self.socket.send_error("A host must be specified")
    elif not data.get("username"):
      self.socket.send_error("A username must be specified")
    else:
      gs.add_player(self.socket, data["host"], data["username"])

  def list_games(self):
    gs.send_waiting_games(self.socket)
