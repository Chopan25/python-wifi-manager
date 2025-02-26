from dataclasses import dataclass
import subprocess


@dataclass
class WiFiNetwork:
    """
    Represents a WiFi network with its properties.

    Attributes:
        used (bool): Indicates whether the network is currently in use.
        bssid (str): The MAC address of the access point.
        ssid (str): The name of the WiFi network.
        mode (str): The mode of the network (e.g., infrastructure, ad-hoc).
        channel (int): The frequency channel the network is operating on.
        rate (str): The maximum data rate of the network.
        signal (int): The signal strength of the network.
        security (str): The security type of the network (e.g., WPA2, Open).
    """
    used: bool
    bssid: str
    ssid: str
    mode: str
    channel: int
    rate: str
    signal: int
    security: str

    def to_dict(self):
        """
        Converts the WiFiNetwork object to a dictionary.

        Returns:
            dict: A dictionary representation of the WiFiNetwork object.
        """
        return {
            'Used': self.used,
            'BSSID': self.bssid,
            'SSID': self.ssid,
            'Mode': self.mode,
            'Channel': self.channel,
            'Rate': self.rate,
            'Signal': self.signal,
            'Security': self.security
        }

    def from_dict(self, data: dict):
        """
        Populates the WiFiNetwork object from a dictionary.

        Args:
            data (dict): A dictionary containing network attributes.

        Returns:
            WiFiNetwork: The updated WiFiNetwork instance.
        """
        self.used = data.get('Used')
        self.bssid = data.get('BSSID')
        self.ssid = data.get('SSID')
        self.mode = data.get('Mode')
        self.channel = data.get('Channel')
        self.rate = data.get('Rate')
        self.signal = data.get('Signal')
        self.security = data.get('Security')
        return self


class WiFiManager:
    """
    A class for managing WiFi networks using `nmcli`.
    """

    @classmethod
    def rescan_networks(cls):
        """
        Triggers a WiFi scan using `nmcli`.

        Returns:
            int: Exit code of the `nmcli` command.
        """
        result = subprocess.run(['sudo', 'nmcli', 'dev', 'wifi', 'rescan'], capture_output=True, text=True)
        return result.returncode

    @classmethod
    def list_networks(cls):
        """
        Lists available WiFi networks.

        Returns:
            list[WiFiNetwork]: A list of available WiFi networks.
        """
        cls.rescan_networks()
        result = subprocess.run(['nmcli', '--terse', 'dev', 'wifi', 'list'], capture_output=True, text=True)
        result = str(result.stdout).split('\n')
        networks = []
        for net_str in result:
            if net_str == '':
                continue
            else:
                networks.append(cls.__format_network(net_str))
        return networks

    @classmethod
    def __format_network(cls, network: str):
        """
        Parses a network string from `nmcli` output into a WiFiNetwork object.

        Args:
            network (str): A single line from `nmcli` output representing a WiFi network.

        Returns:
            WiFiNetwork: The parsed WiFi network object.
        """
        split_line = network.split(':')

        used = split_line[0] == '*'
        bssid = '_'.join(split_line[1:7]).replace('\\_', ':')
        ssid = split_line[7]
        mode = split_line[8]
        channel = split_line[9]
        rate = split_line[10]
        signal = split_line[11]
        security = split_line[13]

        return WiFiNetwork(
            used=used,
            bssid=bssid,
            ssid=ssid,
            mode=mode,
            channel=int(channel),
            rate=rate,
            signal=int(signal),
            security=security
        )

    @classmethod
    def disconnect(cls):
        """
        Disconnects from the current WiFi network.

        Returns:
            int: Exit code of the `nmcli` command.
        """
        result = subprocess.run(['sudo', 'nmcli', 'dev', 'disconnect', 'wlp11s0'], capture_output=True, text=True)
        return result.returncode

    @classmethod
    def connect(cls, network: WiFiNetwork, password: str = ''):
        """
        Connects to a specified WiFi network using `nmcli`.

        Args:
            network (WiFiNetwork): The WiFi network to connect to.
            password (str): The password for the WiFi network.

        Returns:
            int: Exit code of the `nmcli` command.
        """
        net_ssid = network.ssid
        result = subprocess.run(['sudo', 'nmcli', 'dev', 'wifi', 'connect', net_ssid, 'password', password],
                                capture_output=True, text=True)
        return result.returncode
