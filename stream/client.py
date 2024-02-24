from socket import socket, AF_INET, SOCK_STREAM
import _thread as threading

from utils.abstract import AbstractClass


class AbstractStreamClientHandler(AbstractClass):
    def __init__(self):
        super().__init__(AbstractStreamClientHandler)

    @AbstractClass.abstract_method
    def on_receive(self, data):
        ...


class StreamClient(socket):
    def __init__(
        self,
        socket_handler_class,
        host,
        port,
        family=AF_INET,
        type=SOCK_STREAM,
    ):
        super().__init__(family, type)

        self.__socket_handler_class = socket_handler_class

        self.__host = host

        self.__port = port

    def __perform_loop(self):
        data = self.recv(1024)

        socket_handler = self.__socket_handler_class()

        threading.start_new_thread(socket_handler.on_receive, args=(data,))

    def start(self):
        self.connect((self.__host, self.__port))

        print(f"Start StreamClient: HOST={self.__host} PORT={self.__port}")

        while True:
            self.__perform_loop()
