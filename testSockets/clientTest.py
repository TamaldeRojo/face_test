import socket,cv2,pickle,struct 

def clientConn():
    data = b""
    payload_size = struct.calcsize('Q')
    while True:
        while len(data)<payload_size:
            packet = client_socket.recv(4*1024)
            if not packet: break
            data += packet 
        packet_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packet_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Received", frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            client_socket.close()
            break
    
def send_number(number: int):
    client_socket.send(str(number).encode())
    print(f"[+] Number {number} sent to the server.")
    
if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.56.1'
    port = 5050
    client_socket.connect((host_ip,port))
    
    number = int(input("Enter a number from 1 to 5: "))
    send_number(number)
    clientConn()
