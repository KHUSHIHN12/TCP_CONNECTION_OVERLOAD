# TCP_CONNECTION_OVERLOAD
# TCP Load Testing with Load Balancer and Backend Servers

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Project Overview

This project demonstrates handling **TCP connection establishment and termination** in high-load environments using a layered architecture:

- **Backend TCP Servers** using non-blocking sockets and `select` for scalable multiplexing.
- A **Load Balancer** that distributes client connections across backend servers using round-robin.
- A **Load Test Client Simulator** to generate concurrent TCP connections and messages.

---

## Components

### ✅ Backend TCP Server (`server_polling.py`)
- Non-blocking TCP server using `select` to handle multiple clients in a single thread.
- Listens on a configurable port (default `5000`).
- Accepts connections, reads client messages, replies with acknowledgments.
- Cleans up on client disconnect or errors.

### ✅ Load Balancer (`load_balancer.py`)
- Listens on port `4000` for client connections.
- Maintains a list of backend servers (default `localhost:5000`, `localhost:5001`).
- Forwards incoming connections to backend servers using round-robin.
- Uses threads to pipe data bidirectionally between client and backend server sockets.

### ✅ Load Test Client (`load_test_client.py`)
- Simulates multiple concurrent clients connecting to the load balancer.
- Each client sends a message and waits for a response before disconnecting.
- Supports configurable number of clients and staggered connection delays.

---

## 🔧 Getting Started

### Prerequisites

- Python 3.6 or higher installed.
- No external packages required (`socket`, `select`, `threading`, `time` are all built-in).

---

## 🚀 How to Run

### Step 1: Start Backend Servers

In separate terminal windows, run:

```bash
Terminal 1:
python server_polling.py 5000
Terminal 2:
python server_polling.py 5001
Terminal 3:
python load_balancer.py
Terminal 4:
python load_test_client.py
