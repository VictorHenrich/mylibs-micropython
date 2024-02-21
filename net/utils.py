import network


class NetUtils:
    __wlan_instance = None

    @classmethod
    def connect_wifi(cls, network_name, network_password):
        cls.__wlan_instance = network.WLAN(network.STA_IF)

        cls.__wlan_instance.active(True)

        cls.__wlan_instance.connect(network_name, network_password)

    @classmethod
    def disconnect_wifi(cls):
        if not cls.__wlan_instance:
            return

        cls.__wlan_instance.close()

    @classmethod
    def wifi_connected(cls):
        if not cls.__wlan_instance:
            return

        return cls.__wlan_instance.isconnected()
