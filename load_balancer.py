import socket
import threading

backend_servers = [("localhost", 5000), ("localhost", 5001)]
current_server = 0
server_lock = threading.Lock()

def handle_client(client_sock):
    global current_server
    try:
        with server_lock:
            target_host, target_port = backend_servers[current_server]
            current_server = (current_server + 1) % len(backend_servers)
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.connect((target_host, target_port))
        threading.Thread(target=pipe, args=(client_sock, server_sock), daemon=True).start()
        threading.Thread(target=pipe, args=(server_sock, client_sock), daemon=True).start()
    except ExcepƟon as e:
        print(f"[ERROR] Failed to connect to backend {target_host}:{target_port} - {e}")
        client_sock.close()

def pipe(source, dest):
    try:
        while True:
            data = source.recv(1024)
            if not data:
                break
            dest.sendall(data)
    except:
        pass
    finally:
        try:
            dest.shutdown(socket.SHUT_WR)
        except:
            pass
        source.close()
        dest.close()

def run_load_balancer(host='localhost', port=4000):
    lb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lb.bind((host, port))
    lb.listen()
    print(f"[LOAD BALANCER] Listening on {host}:{port}")
    while True:
        client_sock, addr = lb.accept()
        print(f"[FORWARDING] Client {addr} connected")
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    run_load_balancer()
