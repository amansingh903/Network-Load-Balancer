import socket
import threading
import sys

def handle_client(client_socket, address, server_id):
    print(f"[Backend {server_id}] Connection from {address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response = f"Hello from backend {server_id}".encode()
            client_socket.sendall(response)
    finally:
        print(f"[Backend {server_id}] Connection closed: {address}")
        client_socket.close()

def start_server(host, port, server_id):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[Backend {server_id}] Echo server listening on {host}:{port}")
    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock, addr, server_id), daemon=True).start()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <port> <server_id>")
        sys.exit(1)
    HOST = "127.0.0.1"
    PORT = int(sys.argv[1])
    SERVER_ID = sys.argv[2]
    start_server(HOST, PORT, SERVER_ID) 