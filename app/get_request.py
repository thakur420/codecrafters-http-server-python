import sys
from pathlib import Path
import utils
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
    path = utils.extract_path(request)
    str = extract_body(request,path)
    if str == None:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        content_type = get_content_type(path)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(str)}\r\n\r\n{str}"
        client_socket.sendall(response.encode("utf-8")) 