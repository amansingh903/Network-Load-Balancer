# Python Network Load Balancer

A multi-threaded TCP load balancer built in Python that distributes incoming client requests across multiple backend servers using a round-robin algorithm. The project includes fault tolerance, concurrent client handling, and demonstration scripts for backend servers and clients.

## Features

- Round-robin load balancing
- Multi-threaded request handling
- Fault-tolerant backend selection
- Simulated backend echo servers
- Interactive client for testing
- Modular and extensible architecture

## Project Structure

| File               | Description                                                              |
|--------------------|--------------------------------------------------------------------------|
| `load_balancer.py` | Main load balancer that distributes requests across available backends  |
| `backend_server.py`| Simple echo server simulating a backend server                          |
| `client_demo.py`   | Command-line client for sending messages to the load balancer           |

## How to Run

### 1. Start Backend Servers

Run each backend server on a separate terminal with a unique port and ID:

```bash
python backend_server.py 9001 A
python backend_server.py 9002 B
python backend_server.py 9003 C
````

### 2. Start the Load Balancer

```bash
python load_balancer.py
```

By default, it listens on `127.0.0.1:8000`.

### 3. Run the Client

```bash
python client_demo.py
```

Enter messages via the terminal to test request routing through the load balancer.

## Concepts Demonstrated

* TCP socket programming
* Thread-based concurrency
* Load balancing algorithms (round-robin)
* Basic fault handling and backend failover
* Scalable client-server architecture

## Possible Extensions

* Add support for least-connections or IP-hash routing
* Implement health checks for backends
* Add HTTPS/TLS support
* Create a web dashboard for monitoring traffic
* Dockerize and deploy in a containerized environment
