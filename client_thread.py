import sys
import socket
import logging
import threading
import time


def send_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("Opening socket")

    server_address = ('localhost', 45000)
    logging.warning(f"Connecting to server at {server_address}")
    sock.connect(server_address)

    try:
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] Sending message: {message}")
        sock.sendall(message.encode())
        data = sock.recv(32)
        logging.warning(f"[RECEIVED FROM SERVER] {data}")
    finally:
        logging.warning("Closing socket")
        sock.close()


def create_thread():
    t = threading.Thread(target=send_data)
    t.start()
    t.join()


if __name__ == '__main__':
    thread_count = 0
    start_time = time.time()
    while time.time() - start_time < 10:
        create_thread()
        thread_count += 1
    logging.warning(f"Total threads created: {thread_count}")
