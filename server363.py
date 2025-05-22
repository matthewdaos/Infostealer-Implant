import os
import sys
import socket
import time
from datetime import datetime
from cryptography.fernet import Fernet
import io
import zipfile

FERNET_KEY = "YOUR_FERNET_KEY"
fernet = Fernet(FERNET_KEY)

BUFFER_SIZE = 4096

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d:%H:%M:%S')

def save_and_extract(data, client_ip):
    decrypted = fernet.decrypt(data)
    timestamp = get_timestamp()
    dir_name = f"{timestamp}_{client_ip}"
    os.makedirs(dir_name, exist_ok=True)

    archive_io = io.BytesIO(decrypted)
    with zipfile.ZipFile(archive_io, 'r') as zipf:
        zipf.extractall(path=dir_name)

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, int(port)))
        s.listen()
        print(f"[*] Listening on {host}:{port}")
        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"[+] Connection from {addr[0]}")
                    data = b''
                    while True:
                        chunk = conn.recv(BUFFER_SIZE)
                        if not chunk:
                            break
                        data += chunk
                    save_and_extract(data, addr[0])
        except KeyboardInterrupt:
            print("\n[!] Server shutdown requested. Exiting gracefully.")
                 

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./server363 <ip> <port>")
        sys.exit(1)
    start_server(sys.argv[1], sys.argv[2])
