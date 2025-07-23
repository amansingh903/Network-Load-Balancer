import socket

LB_HOST = "127.0.0.1"
LB_PORT = 8000

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((LB_HOST, LB_PORT))
        print("Type messages to send to the server. Type 'exit' to quit.")
        while True:
            message = input("Message: ")
            if message.lower() == 'exit':
                break
            sock.sendall(message.encode())
            response = sock.recv(4096)
            print(f"Received from server: {response.decode()}") 