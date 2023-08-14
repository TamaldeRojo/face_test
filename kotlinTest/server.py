import socket,cv2
import time

cap = cv2.VideoCapture(0)
host_name = socket.gethostname()
#HOST = socket.gethostbyname(host_name)
HOST = "192.168.0.7"
PORT = 5050
correo = "defaultServer@gmail.com"
correos = ['list@gmail.com','listtest@gmail.com']

def save_emails_to_file():
    with open("emails.txt", "w") as file:
        for email in correos:
            file.write(email + "\n")
            
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server is listening on {HOST}:{PORT}")

    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to client: {addr}" )
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            print("No data")
            break
        elif "@" in data:
            print(f"Correo nuevo: {data}")
            correos.append(data)
            save_emails_to_file()
            client_socket.close()
            continue
        

    # Close the connection
    client_socket.close()
    server_socket.close()
