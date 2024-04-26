from typing import Mapping, Any

class NetUtils:
    @classmethod
    def connect_wifi(cls, network_name: str, network_password: str) -> None:
        """
        Connect to the WiFi network

        Parameters
        -----------

        network_name: str
            Name of the network being configured

        network_password: str
            Password of the network being configured
        """
    @classmethod
    def disconnect_wifi(cls) -> None:
        """
        Disconnect to the WiFi network
        """
    @classmethod
    def wifi_connected(cls) -> bool:
        """
        Check if wifi is connected
        """
    @classmethod
    def get_config(cls) -> Mapping[str, Any]:
        """
        Capture network information
        """
