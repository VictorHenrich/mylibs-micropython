from typing import Mapping, Any
from unittest import TestCase
import requests
import json

from stream.server import StreamServer, AbstractStreamConnectionHandler
from stream.client import StreamClient, AbstractStreamClientHandler


class CustomCase(TestCase):
    class StreamConnectionHandler(AbstractStreamConnectionHandler):
        __MAPPERS: Mapping[str, Any] = {
            "led_red": 17,
            "led_blue": 18,
            "led_yellow": 19,
            "led_green": 20,
        }

        __WIT_IA_URL: str = "https://api.wit.ai"

        __WIT_TOKEN: str = "IAL5B7YCCKLCAINBRUV75RUN3DAZCR4J"

        def __get_understanding_wit(self, response: requests.Response) -> str:
            response_data: Mapping[str, Any] = response.json()

            if not response_data.get("entities"):
                raise Exception(
                    "The type of pin was not identified by the text passed!"
                )

            pin_data: Mapping[str, Any] = response_data["entities"][
                "pin_name:pin_name"
            ][0]

            return pin_data["value"]

        def __integrate_wit(self, text: str) -> str:
            url: str = f"{self.__class__.__WIT_IA_URL}/message"

            query_params: Mapping[str, Any] = {"q": text}

            headers: Mapping[str, Any] = {
                "Authorization": f"Bearer {self.__class__.__WIT_TOKEN}"
            }

            response: requests.Response = requests.get(
                url, params=query_params, headers=headers
            )

            return self.__get_understanding_wit(response)

        def __get_pin(self, pin_name: str) -> int:
            try:
                return self.__class__.__MAPPERS[pin_name]

            except KeyError:
                raise Exception(f"Pin Name '{pin_name}' is not configured!")

        def on_receive(self, data: bytes) -> None:
            print(f"CONNECTION HENDLER DATA: {data}")

            dict_data: Mapping[str, Any] = json.loads(data)

            pin_name: str = self.__integrate_wit(dict_data["text"])

            pin: int = self.__get_pin(pin_name)

            send_data: Mapping[str, Any] = {"pin": pin}

            self.socket.sendall(json.dumps(send_data).encode("utf-8"))

    class StreamClientHandler(AbstractStreamClientHandler):
        def on_receive(self, data: bytes) -> None:
            print(f"\nCLIENT HANDLER DATA: {data}")

    def setUp(self) -> None:
        self.__port: int = 5000

    def test_server(self) -> None:
        stream_server: StreamServer = StreamServer(
            CustomCase.StreamConnectionHandler, host="0.0.0.0", port=self.__port
        )

        stream_server.start()

    def test_client(self) -> None:
        stream_client: StreamClient = StreamClient(
            CustomCase.StreamClientHandler, host="192.168.15.105", port=self.__port
        )

        stream_client.start()

        while True:
            text: str = input("Command: ")

            stream_client.send_data({"text": text})
