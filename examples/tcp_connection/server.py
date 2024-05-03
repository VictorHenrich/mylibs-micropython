from machine import Pin
import _thread as threading
import json

from stream.server import StreamServer, AbstractStreamConnectionHandler
from utils.net import NetUtils


class CustomPin(Pin):
    def __init__(self, pin_id, pin_mode=Pin.IN, pin_value=False):
        super().__init__(pin_id, pin_mode)

        self.__pin_id = pin_id

        self.__pin_mode = pin_mode

        self.__pin_value = pin_value

    @property
    def pin_id(self):
        return self.__pin_id

    @property
    def pin_mode(self):
        return self.__pin_mode

    @property
    def pin_value(self):
        return self.__pin_value

    @pin_mode.setter
    def pin_mode(self, pin_mode):
        self.__pin_mode = pin_mode

    @pin_value.setter
    def pin_value(self, pin_value):
        self.__pin_value = pin_value

    def change(self):
        self.init(mode=self.__pin_mode, value=self.__pin_value)


PINS = [
    CustomPin(pin_id=23),
    CustomPin(pin_id=22),
    CustomPin(pin_id=21),
]


class StreamServerHandler(AbstractStreamConnectionHandler):
    __mapped_mode = {("in",): Pin.IN, ("out",): Pin.OUT}

    def __get_mode(self, mode):
        for mode_keys, mode_value in StreamServerHandler.__mapped_mode.items():
            if mode.lower() in mode_keys:
                return mode_value

        return Pin.IN

    def on_receive(self, data):
        print(f"Data: {data}")

        pin_data = json.loads(data)

        for board_pin in PINS:
            if board_pin.pin_id == pin_data["id"]:
                board_pin.pin_mode = self.__get_mode(pin_data["mode"])

                board_pin.pin_value = pin_data["value"]

                board_pin.change()


class TCPService(StreamServer):
    def __init__(self, host, port):
        super().__init__(
            socket_connection_class=StreamServerHandler, host=host, port=port
        )

    def start(self):
        threading.start_new_thread(super().start, ())


tcp_service = TCPService(host="0.0.0.0", port=5000)

service_run = False

NetUtils.connect_wifi(network_name="ANA", network_password="100831122104")


while True:
    if NetUtils.wifi_connected() and not service_run:
        print("WIFI CONNECTED!")

        network_configs = NetUtils.get_config()

        print(f"NETWORK CONFIGS: {network_configs}")

        service_run = True

        tcp_service.start()

    if service_run:
        for board_pin in PINS:
            board_pin.value(board_pin.pin_value)
