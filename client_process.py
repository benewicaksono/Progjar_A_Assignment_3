import sys
import socket
import logging
from multiprocessing import Process
import time


def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('localhost', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] sending {message}")
        sock.sendall(message.encode())
        data = sock.recv(32)
        logging.warning(f"[DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning("closing")
        sock.close()
    return


def create_process():
    p = Process(target=kirim_data)
    p.start()
    p.join()


if __name__ == '__main__':
    process_count = 0
    start_time = time.time()
    while time.time() - start_time < 10:
        create_process()
        process_count += 1
    logging.warning(f"Total processes created: {process_count}")
