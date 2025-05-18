import socket
import threading
import time

def simulate_client(client_id, message="Hello from client", delay=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 4000))
        print(f"[CLIENT-{client_id}] Connected")
        sock.sendall(f"{message} #{client_id}".encode())
        response = sock.recv(1024)
        print(f"[CLIENT-{client_id}] Server response: {response.decode().strip()}")
        time.sleep(delay)
    except Exception as e:
        print(f"[CLIENT-{client_id}] Error: {e}")

    finally:
        sock.close()

def run_load_test(client_count=20):
    threads = []
    for i in range(client_count):
        t = threading.Thread(target=simulate_client, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(0.1)  # Stagger connecƟons slightly
    for t in threads:
        t.join()

if __name__ == "__main__":
    run_load_test(client_count=50)
