import socket
import concurrent.futures as cf
import sys
from pathlib import Path

def extract_path(request):
    request_lines = request.splitlines()
    if request_lines:
        request_line = request_lines[0]
        parts = request_line.split()
        if len(parts) > 1:
            return parts[1]
        return ""
    
# GET Request processing code   
def extract_header(request,header):
    response = [line for line in request.splitlines() if header in line][0]
    if len(response) > 0 :
        return response.split(':')[-1].strip()
    return None

def read_file_content(file_name):
    try:
        dir = Path(sys.argv[2]) if len(sys.argv) >= 2 else Path()
        file_path = dir / file_name
        with open(file_path,"rb") as f:
            data = f.read()
            return data.decode("utf-8")
    except FileNotFoundError:
        print(f"file {file_path} does not exist ...")
        return None
        
def extract_body(request,path):
    if "/files" in path:
       file_name = path.split("/")[-1]
       return read_file_content(file_name)
    if "/echo" in path :
        val = path.split("/")[-1]
        return val if val != "echo" else "" 
    if "/user-agent" in path:
        return extract_header(request,"User-Agent")
    if len(path) == 1 and "/" in path:
        return ""
    return None

def get_content_type(path):
    if "/file" in path:
        return "application/octet-stream"
    return "text/plain"

def handle_get_request(request,client_socket):
    path = extract_path(request)
    str = extract_body(request,path)
    if str == None:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        content_type = get_content_type(path)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(str)}\r\n\r\n{str}"
        client_socket.sendall(response.encode("utf-8")) 

# POST Request processing code

def extract_data(request):
    str = ""
    for i,line in enumerate(request.splitlines()):
        if i >= 7: # skip request line and headers 
            str += line
    return str 

def save_to_file(path,data):
    file_name = path.split("/")[-1] if "/files" in path else "" 
    dir = Path(sys.argv[2]) if len(sys.argv) >= 2 else Path()
    file_path = dir / file_name
    with open(file_path,"w") as f:
        f.write(data)
    
def handle_post_request(request,client_socket):
    path = extract_path(request)
    data = extract_data(request)
    save_to_file(path,data)
    client_socket.sendall(b"HTTP/1.1 201 Created\r\n\r\n")

# Handle Client Request
def handle_client(client_socket):
    try :
        request = client_socket.recv(1024).decode("utf-8")
        if "GET" in request:
            handle_get_request(request,client_socket)
        elif "POST" in request:
            handle_post_request(request,client_socket)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    print("Logs from your program will appear here!")
    with socket.create_server(("localhost",4221)) as server_socket:
        server_socket.listen() 
        with cf.ThreadPoolExecutor() as executor:
            while True:  
                client_socket, _ = server_socket.accept()
                executor.submit(handle_client, client_socket)

                
if __name__ == "__main__":
    main()
