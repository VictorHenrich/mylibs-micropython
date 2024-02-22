from bluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_WRITE

from utils.char import CharUtils
from patterns.abstract import AbstractClass


class BluetoothServerParams:
    def __init__(
        self,
        ble,
        uart_transmitter,
        uart_receiver,
        transmitter_handler,
        receiver_handler,
    ) -> None:
        self.__ble = ble

        self.__uart_transmitter = uart_transmitter

        self.__uart_receiver = uart_receiver

        self.__transmitter_handler = transmitter_handler

        self.__receiver_handler = receiver_handler

    @property
    def ble(self):
        return self.__ble

    @property
    def uart_transmitter(self):
        return self.__uart_transmitter

    @property
    def uart_receiver(self):
        return self.__uart_receiver

    @property
    def transmitter_handler(self):
        return self.__transmitter_handler

    @property
    def receiver_handler(self):
        return self.__receiver_handler


class BluetoothEventHandler(AbstractClass):
    def __init__(self, event_type: int) -> None:
        self.__event_type: int = event_type

    @property
    def event_type(self) -> int:
        return self.__event_type

    @AbstractClass.abstract_method
    def handle(self, server_params: BluetoothServerParams, data) -> None:
        ...


class BluetoothServer:
    def __init__(self) -> None:
        self.__listeners: list[BluetoothEventHandler] = []

        self.__server_params = self.__create_and_configure_ble_instance()

    def __handle_events(self, event, data, *args) -> None:
        for listener in self.__listeners:
            if event == listener.event_type:
                listener.handle(self.__server_params, data)

                break

    def __create_and_configure_ble_instance(self):
        UART_UUID = UUID(CharUtils.generate_uuid())

        UART_TX = (
            UUID(CharUtils.generate_uuid()),
            FLAG_NOTIFY,
        )

        UART_RX = (UUID(CharUtils.generate_uuid()), FLAG_WRITE)

        _UART_SERVICE = (
            UART_UUID,
            (UART_TX, UART_RX),
        )

        ble_instance = BLE()

        ((tx_handler, rx_handler),) = ble_instance.gatts_register_services(
            (_UART_SERVICE,)
        )

        ble_instance.irq(self.__handle_events)

        ble_instance.active(True)

        return BluetoothServerParams(
            ble=ble_instance,
            uart_transmitter=UART_TX,
            uart_receiver=UART_RX,
            receiver_handler=rx_handler,
            transmitter_handler=tx_handler,
        )

    def add_event_handler(self, *handlers: BluetoothEventHandler) -> None:
        for handler in handlers:
            self.__listeners.append(handler)

    def start_scan(self, duration: int = 0) -> None:
        self.__server_params.ble.gap_scan(2000, 30000, 30000)

    def stop_scan(self) -> None:
        self.__server_params.ble.gap_scan(None)

    def start_advertise(self, interval: int = 100) -> None:
        self.__server_params.ble.gap_advertise(interval)

    def stop_advertise(self) -> None:
        self.__server_params.ble.gap_advertise(None)

    def add_peripheral(
        self, address_type: int, address: bytes, connection_handler: memoryview
    ) -> None:
        self.__server_params.ble.gap_connect(address_type, address)

    def remove_peripheral(self, connection_handler: memoryview) -> None:
        self.__server_params.ble.gap_disconnect(connection_handler)

    def send_notification(self, data: str) -> None:
        self.__server_params.ble.gatts_notify(
            self.__server_params.transmitter_handler, data.encode("utf-8")
        )
