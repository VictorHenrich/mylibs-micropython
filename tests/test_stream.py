from unittest import TestCase

from stream.server import StreamServer, AbstractStreamConnectionHandler
from stream.client import StreamClient, AbstractStreamClientHandler


class StreamCase(TestCase):
    class StreamConnectionHandler(AbstractStreamConnectionHandler):
        def on_receive(self, data: bytes) -> None:
            print(f"CONNECTION HENDLER DATA: {data}")

    class StreamClientHandler(AbstractStreamClientHandler):
        def on_receive(self, data: bytes) -> None:
            print(f"CLIENT HANDLER DATA: {data}")

    def setUp(self) -> None:
        self.__host: str = "localhost"

        self.__port: int = 5000

    def test_server(self) -> None:
        stream_server: StreamServer = StreamServer(
            StreamCase.StreamConnectionHandler, host=self.__host, port=self.__port
        )

        stream_server.start()

    def test_client(self) -> None:
        stream_client: StreamClient = StreamClient(
            StreamCase.StreamClientHandler, host=self.__host, port=self.__port
        )

        message: bytes = "Isso é apenas um teste".encode("utf-8")

        stream_client.start()

        stream_client.sendall(message)
