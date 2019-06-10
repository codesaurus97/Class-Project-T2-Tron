from Server import Server                # Server interface
from ..Core.Exceptions import ServerError  #ServerError Exception
from Arena import Arena
import socket

class TCPServer(Server):
	"""
	Realization of Server Interface for TCP Server
	"""

	__host = ""                 # Server Host IP
	__port = 0                  # Server Port
	__status = 0                # Server status
	__Arena = None              # Hosted Arena
	__playernumber = 0          # Number of players
	__comm_proto = None         # Communication protocol
	__players = []              # Array of players
	__sock = None # Serversocket
	__settings_locked = False   # Check if server settings are locked

	def __init__(self, host="", port=23456):
		"""
		Initialize TCP Server on the given host IP and port
		Args:
			host (str): IPv4 address of host (any="")
			port (int): Port number of the server
		Raises:
			TypeError: Not valid types
			ValueError: Port Number is invalid
		"""
		if not type(host) == str:
			raise TypeError
		
		if not type(port) == int:
			raise TypeError
		
		if port not in range(0,2**16-1):
			raise ValueError
		try:
			# Create IPv4 TCP Socket
			self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.__sock.bind((host, port))
		except Exception as e:
			# Raise a ServerError
			raise ServerError(str(e))
	
	def setArena(self, arena):
		"""
		Set the arena of the game server

		Args:
			arena (Arena): Arena object created for the game
		
		Raises:
			TypeError: The object is not an arena.
			ServerError: The arena type doesn't exist on the server, or ...
				the server is still running.
		"""

		if not type(arena) == Arena:
			raise TypeError
		
		if self.__settings_locked:
			raise ServerError("Cannot change the arena, while the server is running")
		
		self.__Arena = arena
	
	def getArena(self):
		"""
		Get the arena the game server hosts.

		Returns:
			Arena: Currently active arena object
		"""
		return self.__Arena

	
	def setPlayerNumber(self, players):
		"""
		Set the number of the players who will play the game
		
		Args:
			players (int): Number of the players the server starts the game with.
		
		Raises:
			TypeError: players is not an integer
			ValueError: Players is not a valid number
			ServerError: The server is still running.
		"""
		if not type(players) == int:
			raise TypeError
		
		if not players in range(0,100):
			raise ValueError
		
		if(self.__settings_locked):
			raise ServerError("Cannot update player number, the server is running")
		
		# Set the player number
		self.__playernumber = players

	
	def getPlayerNumber(self):
		"""
		Get the number of players currently on the server.

		Returns:
			int: Number of players
		"""

		return self.__playernumber
	
	def getPlayers(self):
		"""
		Get the collection of players connected to the server

		Returns:
			iter: List of the players connected to the server
		
		Raises:
			ServerError: Server is not running
		"""
		# TODO: Add ServerError when the server is not running
		return self.__players

	def Start(self):
		
		try:
			# Start listening on socket
			self.__sock.listen()
			client_sock = self.__sock.accept()
			# TODO: Start new thread for client_socket
		except:
			pass


