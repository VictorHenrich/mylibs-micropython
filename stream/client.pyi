from typing import Union, Type
from socket import socket, SocketKind, AddressFamily, AF_INET, SOCK_STREAM

from patterns.abstract import AbstractClass

class StreamClientHandler(AbstractClass):
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
        socket_handler_class: Type[StreamClientHandler],
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
