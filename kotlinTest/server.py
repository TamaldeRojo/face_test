import socket

# Set the host and port for the server
host_name = socket.gethostname()
HOST = socket.gethostbyname(host_name)
PORT = 5050

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}")

# Accept a client connection


# Receive data from the client and send a response
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connected to client: {addr}" )
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print(f"Received from client: {data}")
    response = "Hello from server!"
    #client_socket.send(response.encode())

# Close the connection
client_socket.close()
server_socket.close()
