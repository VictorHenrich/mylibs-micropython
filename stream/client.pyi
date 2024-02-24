from typing import Union, Type, Any
from socket import socket, SocketKind, AddressFamily, AF_INET, SOCK_STREAM

from utils.abstract import AbstractClass

class AbstractStreamClientHandler(AbstractClass):
    @AbstractClass.abstract_method
    def on_receive(self, data: bytes) -> None:
        """
        Method responsible for the arrival of notifications from customers.

        Parameters
        -----------

        data: bytes
            Notification receipt data
        """

class StreamClient(socket):
    def __init__(
        self,
        socket_handler_class: Type[AbstractStreamClientHandler],
        host: str,
        port: Union[str, int],
        family: AddressFamily = AF_INET,
        type: SocketKind = SOCK_STREAM,
    ) -> None: ...
    def __perform_loop(self) -> None: ...
    def start(self) -> None:
        """
        Start socket client
        """
    def send_data(self, data: Any) -> None:
        """
        Send a message to the server

        Parameters
        -----------

        data: Any
            Data to be sent
        """
