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

        cls.__wlan_instance = None

    @classmethod
    def wifi_connected(cls):
        if not cls.__wlan_instance:
            return False

        return cls.__wlan_instance.isconnected()

    @classmethod
    def get_config(cls):
        if cls.__wlan_instance is None:
            return

        ip, subnet_mask, gateway, dns_server = cls.__wlan_instance.ifconfig()

        return {
            "ip": ip,
            "subnet_mask": subnet_mask,
            "gateway": gateway,
            "dns_server": dns_server,
        }
