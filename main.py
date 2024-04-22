import socket
import platform
import subprocess
import urllib.parse

# Define the port to listen on
PORT = 54321

# Define the special parameter name to lock the screen
LOCK_PARAM = 'key'
LOCK_KEY = 'KEYDATA'

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_socket.bind(('', PORT))

# Listen for incoming connections
server_socket.listen(1)

print(f"Server listening on port {PORT}")

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    client_socket, addr = server_socket.accept()
    print('Got connection from', addr)

    # Get the request data
    request_data = client_socket.recv(1024).decode()

    # Parse the request data to get the query parameters
    query_params = urllib.parse.parse_qs(
        request_data.split('\n')[0].split(' ')[1][2:])

    # Check if the lock parameter is set and if the key matches
    if LOCK_PARAM in query_params and query_params[LOCK_PARAM][0] == LOCK_KEY:
        # Lock the screen based on the operating system
        if platform.system() == 'Windows':
            # Windows
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
        else:
            # Ubuntu
            subprocess.run(['gnome-screensaver-command', '-l'])
        print('Screen locked')
    else:
        print('Lock parameter not found or key does not match')

    # Close the connection
    client_socket.close()
