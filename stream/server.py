from socket import socket, AF_INET, SOCK_STREAM
import _thread as threading

from utils.abstract import AbstractClass


class AbstractStreamConnectionHandler(AbstractClass):
    def __init__(self, socket, address):
        super().__init__(AbstractStreamConnectionHandler)

        self.__socket = socket

        self.__address = address

    @property
    def socket(self):
        return self.__socket

    @property
    def address(self):
        return self.__address

    @AbstractClass.abstract_method
    def on_receive(self, data):
        ...


class StreamServer(socket):
    def __init__(
        self,
        socket_connection_class,
        host="localhost",
        port=5000,
        family=AF_INET,
        type=SOCK_STREAM,
    ):
        super().__init__(family, type)

        self.__socket_connection_class = socket_connection_class

        self.__host = host

        self.__port = port

        self.__connections = []

    def __handle_client_connection(self, client_connection):
        while True:
            received_data = client_connection.socket.recv(1024)

            client_connection.on_receive(received_data)

    def __perform_loop(self):
        client_socket, address = self.accept()

        client_connection = self.__socket_connection_class(client_socket, address)

        self.__connections.append(client_connection)

        threading.start_new_thread(
            self.__handle_client_connection, (client_connection,)
        )

    def start(self):
        self.bind((self.__host, self.__port))

        self.listen()

        print(f"Start StreamServer: HOST={self.__host} PORT={self.__port}")

        while True:
            self.__perform_loop()
