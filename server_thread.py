import socket
import threading
import logging
import time


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(64)
            if data:
                logging.warning(
                    f"[SERVER] received {data} from {self.address}")

                if data.startswith(b'TIME') and data.endswith(b'\r\n'):
                    current_time = time.strftime("%H:%M:%S")
                    response = f"JAM {current_time}" + "\r\n"
                    logging.warning(
                        f"[SERVER] sending {response} to {self.address}")
                    self.connection.sendall(response.encode('utf-8'))
                else:
                    response = "REJECTED\r\n"
                    logging.warning(
                        f"[SERVER] sending {response} to {self.address}")
                    self.connection.sendall(response.encode('utf-8'))
            else:
                break

        self.connection.close()


class TimeServer(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.warning("Server listening on port 45000...")

        while True:
            connection, address = self.my_socket.accept()
            logging.warning(f"Connection from {address}")

            client_thread = ProcessTheClient(connection, address)
            client_thread.start()
            self.the_clients.append(client_thread)


def main():
    svr = TimeServer()
    svr.start()


if __name__ == "__main__":
    main()
