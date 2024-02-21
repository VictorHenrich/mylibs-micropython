from typing import Union, Type
from socket import socket, SocketKind, AddressFamily, AddressInfo, AF_INET, SOCK_STREAM
from abc import ABC

class AbstractSocketConnection(ABC):
    def __init__(self, socket: socket, address: AddressInfo) -> None: ...
    def on_receive(self, data: bytes) -> None:
        """
        Method responsible for the arrival of notifications from customers.

        Parameters
        -----------

        data: bytes
            Notification receipt data
        """

class SocketServer(socket):
    def __init__(
        self,
        socket_connection_class: Type[AbstractSocketConnection],
        host: str = "localhost",
        port: Union[str, int] = 5000,
        family: AddressFamily = AF_INET,
        type: SocketKind = SOCK_STREAM,
    ) -> None: ...
    def __handle_client_connection(
        self, client_connection: AbstractSocketConnection
    ) -> None: ...
    def __perform_loop(self) -> None: ...
    def start(self) -> None:
        """
        Start the socket server.
        """
