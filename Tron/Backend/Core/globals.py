# Global configuration of BACKEND classes

LOBBY_DISCOVERY_PORT = 54000
LOBBY_DISCOVERY_ADDR = "255.255.255.255"
LOBBY_PORT_RANGE = range(54010, 54100 + 1)
LOBBY_DISCOVERY_RECV_SIZE = 1024
LOBBY_DISCOVER_TIMEOUT = 1 # Wait for broadcast responses only 2 seconds
DEFAULT_CONTROL_PROTOCOL_PORT = 54001

CONTROL_PROTOCOL_RECV_SIZE = 1024
CLIENT_FEATURES = ['BASIC', 'JSONCOMM'] # LIST of the client features
SERVER_FEATURES = ['BASIC', 'JSONCOMM'] # List of server features

SERVER_GAMES = ['Tron']

UDP_RECV_BUFFER_SIZE = 1024

MAX_MATRIX_SIZE = (20,20)

