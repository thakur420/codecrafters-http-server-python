import socket
import time
import concurrent.futures as cf

def handle_client(client_socket):
    try :
        request = client_socket.recv(1024).decode("utf-8")
        print("processing client request")
        time.sleep(10)
        client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
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
                client_socket,addr = server_socket.accept()
                executor.submit(handle_client, client_socket)
                
if __name__ == "__main__":
    main()
