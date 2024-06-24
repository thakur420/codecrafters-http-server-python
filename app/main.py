# Uncomment this to pass the first stage
import socket
def extract_path(request):
    request_lines = request.splitlines()
    if request_lines:
        request_line = request_lines[0]
        parts = request_line.split()
        if len(parts) > 1:
            part = parts[1]
            return part
    return None

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221))
    client_socket, addr = server_socket.accept() # wait for client
    # print(f"Connected by {addr}")
    request = client_socket.recv(1024).decode("utf-8")
    # print(f"Request : {request}")
    path = extract_path(request)
    if path == "/":
        client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        
if __name__ == "__main__":
    main()
