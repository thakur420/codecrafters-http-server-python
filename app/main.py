import socket
import time
import concurrent.futures as cf
def extract_header(request,header):
    response = [line for line in request.splitlines() if header in line][0]
    if len(response) > 0 :
        return response.split(':')[-1].strip()
    return None

def extract_body(request,path):
    if "/echo" in path :
        val = path.split("/")[-1]
        return val if val != "echo" else "" 
    if "/user-agent" in path:
        return extract_header(request,"User-Agent")
    if len(path) == 1 and "/" in path:
        return ""
    return None

def extract_path(request):
    request_lines = request.splitlines()
    if request_lines:
        request_line = request_lines[0]
        parts = request_line.split()
        if len(parts) > 1:
            return parts[1]
        return ""
    
def handle_client(client_socket):
    try :
        request = client_socket.recv(1024).decode("utf-8")
        # client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
        path = extract_path(request)
        str = extract_body(request,path)
        if str == None:
            client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}"
            client_socket.send(response.encode("utf-8")) 
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
