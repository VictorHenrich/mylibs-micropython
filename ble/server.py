from bluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_WRITE

from utils.char import CharUtils
from patterns.abstract import AbstractClass
from ble.event_types import BluetoothEventTypes


class BluetoothPeripheral:
    def __init__(self, address_type, address_data, connection_handle):
        self.__address_type = address_type

        self.__address_data = address_data

        self.__connection_handle = connection_handle

    @property
    def address_type(self):
        return self.__address_type

    @property
    def address_data(self):
        return self.__address_data

    @property
    def connection_handle(self):
        return self.__connection_handle


class BluetoothServerParams:
    def __init__(
        self,
        ble,
        uart_transmitter,
        uart_receiver,
        transmitter_handler,
        receiver_handler,
    ):
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
    def __init__(self, event_type):
        self.__event_type = event_type

    @property
    def event_type(self):
        return self.__event_type

    @AbstractClass.abstract_method
    def handle(self, server, data):
        ...


class BluetoothServer:
    def __init__(self):
        self.__listeners = []

        self.__peripherals = []

        self.__props = self.__create_and_configure_ble_instance()

    @property
    def peripherals(self):
        return self.__peripherals

    @property
    def props(self):
        return self.__props

    def __handle_events(self, event, data, *args):
        for listener in self.__listeners:
            if event == BluetoothEventTypes.PERIPHERAL_CONNECT:
                conn_handle, address_type, address_data = data

                peripheral = BluetoothPeripheral(
                    address_type, address_data, conn_handle
                )

                self.__peripherals.append(peripheral)

            if event == listener.event_type:
                listener.handle(self.__props, data)

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

    def add_event_handler(self, *handlers):
        for handler in handlers:
            self.__listeners.append(handler)

    def start_scan(self, duration=2000, **kwargs):
        self.__props.ble.gap_scan(duration, **kwargs)

    def stop_scan(self):
        self.__props.ble.gap_scan(None)

    def start_advertise(self, interval=100, **kwargs):
        self.__props.ble.gap_advertise(interval, **kwargs)

    def stop_advertise(self):
        self.__props.ble.gap_advertise(None)

    def add_peripheral(self, peripheral):
        self.__props.ble.gap_connect(peripheral.address_type, peripheral.address_data)

    def remove_peripheral(self, peripheral):
        self.__props.ble.gap_disconnect(peripheral.connection_handler)

    def send_notification(self, data):
        self.__props.ble.gatts_notify(
            self.__props.transmitter_handler, data.encode("utf-8")
        )
