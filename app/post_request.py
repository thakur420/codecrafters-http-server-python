import utils
import sys
from pathlib import Path

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
    path = utils.extract_path(request)
    data = extract_data(request)
    save_to_file(path,data)
    client_socket.sendall(b"HTTP/1.1 201 Created\r\n\r\n")