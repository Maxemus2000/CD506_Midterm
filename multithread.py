import socket,threading
import serverchoice 



server_ip = "localhost"  # server hostname or IP address
port = int(serverchoice.msg)  # server port number


def handle_client(client_socket, addr):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received: {request}")
            # convert and send accept response to the client
            response = request.encode("utf-8")
            client_socket.send(response)
            client_socket.detach()
            changedport = int(request)
            print(f"{addr[0]}:{addr[1]}) changed port to: {changedport}")

            print(f"Now listening on {server_ip}:{changedport}")

    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server(port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen(5)
        print(f"Listening on {server_ip}:{port}")

        # accept a client connection
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}\n")
        # start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
        thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

run_server(port)
