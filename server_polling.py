import socket
import select
import sys

def run_server(host='localhost', port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    server.setblocking(False)
    sockets_list = [server]
    print(f"[SERVER] Listening on {host}:{port}")
    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])
        for s in read_sockets:
            if s == server:
                client_socket, client_address = server.accept()
                print(f"[CONNECT] {client_address} connected")
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
            else:
                try:
                    data = s.recv(1024)
                    if data:
                        print(f"[DATA] {s.getpeername()} sent: {data.decode().strip()}")
                        s.sendall(b"ACK from server")
                    else:
                        raise ConnectionResetError
                except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
                    print(f"[DISCONNECT] {s.getpeername()} disconnected")
                    sockets_list.remove(s)
                    s.close()
                except Exception as e:
                    print(f"[ERROR] {s.getpeername()} - {e}")
                    sockets_list.remove(s)
                    s.close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_server(port=port)
