import socket 

def handle_client_connection(client_socket): 
    request = client_socket.recv(1024).decode() 
    print(f"Received : {request}")
    
    response = f"Server received: {request}"
    client_socket.send(response.encode()) 
    
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind(("localhost", 8080)) 
    server_socket.listen(5) 

    print("Server listening on port 8080 ")

    while True: 
        client_socket, addr = server_socket.accept() 
        print(f"Connected with {addr}")

        handle_client_connection(client_socket)

        client_socket.close()

if __name__ == "__main__":
    main()