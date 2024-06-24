# Uncomment this to pass the first stage
import socket
from pathlib import Path

def extract_path(request):
    request_lines = request.splitlines()
    if request_lines:
        request_line = request_lines[0]
        parts = request_line.split()
        if len(parts) > 1:
            path = Path(parts[1])
            if path.resolve() != Path("/user-agent").resolve():
                return None
    response = [line for line in request_lines if "User-Agent" in line][0]
    # print(response)
    if len(response) > 0 :
        return response.split(':')[-1].strip()
    return None

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 4221))
    client_socket, addr = server_socket.accept() # wait for client
    # print(f"Connected by {addr}")
    request = client_socket.recv(1024).decode("utf-8")
    # print(f"Request : {request}")
    str = extract_path(request)
    if str == None:
        client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}"
        client_socket.send(response.encode("utf-8"))   

if __name__ == "__main__":
    main()
