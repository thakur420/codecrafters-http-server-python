import socket
from get_request import handle_get_request
from post_request import handle_post_request
import concurrent.futures as cf

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
