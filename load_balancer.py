import socket
import threading
import sys
import time

# Configuration: List of backend servers (host, port)
BACKENDS = [
    ("127.0.0.1", 9001),
    ("127.0.0.1", 9002),
    ("127.0.0.1", 9003),
]
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8000

backend_index = 0
backend_lock = threading.Lock()

# Try to connect to a backend, return socket if successful, else None
def try_backend(backend_host, backend_port, timeout=1.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((backend_host, backend_port))
        return s
    except Exception:
        return None

def get_next_backend():
    global backend_index
    with backend_lock:
        backend = BACKENDS[backend_index]
        backend_index = (backend_index + 1) % len(BACKENDS)
    return backend

def handle_client(client_sock, client_addr):
    print(f"[LB] Client connected: {client_addr}")
    try:
        while True:
            client_sock.settimeout(None)
            data = client_sock.recv(4096)
            if not data:
                break
            # Try each backend in round-robin until one is available
            tried = 0
            response = None
            while tried < len(BACKENDS):
                backend_host, backend_port = get_next_backend()
                backend_sock = try_backend(backend_host, backend_port)
                if backend_sock:
                    try:
                        backend_sock.sendall(data)
                        response = backend_sock.recv(4096)
                    finally:
                        backend_sock.close()
                    print(f"[LB] Forwarded message from {client_addr} to backend {backend_host}:{backend_port}")
                    break
                else:
                    print(f"[LB] Backend {backend_host}:{backend_port} is busy or unavailable.")
                    tried += 1
            if response:
                client_sock.sendall(response)
            else:
                client_sock.sendall(b"No backend available. Please try again later.")
    except Exception as e:
        print(f"[LB] Error with client {client_addr}: {e}")
    finally:
        print(f"[LB] Client disconnected: {client_addr}")
        client_sock.close()

def start_load_balancer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(100)
    print(f"[LB] Load balancer listening on {LISTEN_HOST}:{LISTEN_PORT}")
    while True:
        client_sock, client_addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True).start()

if __name__ == "__main__":
    start_load_balancer() 