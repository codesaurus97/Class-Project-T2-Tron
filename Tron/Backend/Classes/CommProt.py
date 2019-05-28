
class CommProt:
	"""
	Client-Server communikation protocol interface
	"""

	def client_ready(self, player):
		"""
		Get a byte coded client ready message

		Args:
			player: Player	Player Object of the Client

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def server_ready(self, game):
		"""
		Get a byte coded server ready message

		Args:
			game: Game	Game object of the current game
							running on the server
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def server_error(self, msg):
		"""
		Get a byte coded server error message

		Args:
			msg: str	Error description (message)
		
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def client_error(self, msg):
		"""
		Get a byte coded server error message

		Args:
			msg: str	Error description (message)
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def client_start(self):
		"""
		Get a byte coded client start message

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def countdown(self, seconds):
		"""
		Get a byte coded countdown message (server-side)

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def ingame(self, game):
		"""
		Get a byte coded in-game message for continous synchronization
			between client and server
		Args:
			game: Game	Game object of the current game running on the
							server
		Return:
			bytes
		"""
		raise NotImplementedError

	def pause(self):
		"""
		Get a byte coded pause request

		Returns:
			bytes
		"""
		raise NotImplementedError

	def continue_game(self, seconds):
		"""
		Get a byte coded continue request

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def ack_pause(self):
		"""
		Get a byte response for acknowledging a pause

		Returns:
			bytes
		"""
		raise NotImplementedError

	def ack_continue(self):
		"""
		Get a byte response for acknowledging a continue_game action

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def exit_game(self):
		"""
		Get a byte request for exiting a running game
		
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def end_game(self):
		"""
		Get a byte request for ending a running game

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def revenge(self):
		"""
		Get a byte request for requesting a revenge

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def ack_revenge(self):
		"""
		Get a byte response for accepting a revenge

		Returns:
			bytes
		"""
		raise NotImplementedError

	
