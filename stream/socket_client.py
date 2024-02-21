from socket import socket, AF_INET, SOCK_STREAM
import _thread as threading

from patterns.abstract import AbstractClass


class SocketClientHandler(AbstractClass):
    @AbstractClass.abstract_method
    def on_receive(self, data):
        ...


class SocketClient(socket):
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

        socket_handler: SocketClientHandler = self.__socket_handler_class()

        threading.start_new_thread(socket_handler.on_receive, args=(data,))

    def start(self):
        self.connect((self.__host, self.__port))

        while True:
            self.__perform_loop()
