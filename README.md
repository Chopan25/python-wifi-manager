# WiFi Manager Module

This module provides a `WiFiManager` class for managing WiFi networks using `nmcli`,
and a `WiFiNetwork` dataclass to represent individual networks.

## Classes

### WiFiNetwork
A dataclass representing a WiFi network.

#### Attributes:
- **used (bool):** Indicates whether the network is currently in use.
- **bssid (str):** The MAC address of the access point.
- **ssid (str):** The name of the WiFi network.
- **mode (str):** The mode of the network (e.g., infrastructure, ad-hoc).
- **channel (int):** The frequency channel the network is operating on.
- **rate (str):** The maximum data rate of the network.
- **signal (int):** The signal strength of the network.
- **security (str):** The security type of the network (e.g., WPA2, Open).

#### Methods:
- **to_dict()**
  - Converts the `WiFiNetwork` object to a dictionary.
- **from_dict(data: dict)**
  - Populates the `WiFiNetwork` object from a dictionary.

### WiFiManager
A class for managing WiFi networks using `nmcli`.

#### Methods:
- **rescan_networks()**
  - Triggers a WiFi scan using `nmcli`.
  - **Returns:** Exit code of the `nmcli` command.

- **list_networks()**
  - Lists available WiFi networks, returning a list of `WiFiNetwork` objects.
  - **Returns:** List of `WiFiNetwork` objects.

- **disconnect()**
  - Disconnects from the current WiFi network.
  - **Returns:** Exit code of the `nmcli` command.

- **connect(network: WiFiNetwork, password: str)**
  - Connects to the specified WiFi network using a password.
  - **Parameters:**
    - `network` (WiFiNetwork): The WiFi network to connect to.
    - `password` (str): The password for the WiFi network.
  - **Returns:** Exit code of the `nmcli` command.

## Installation
To use this module, you must have NetworkManager installed on your Linux system.

### Install NetworkManager
Run the following command:
```sh
sudo apt install network-manager # Debian/Ubuntu
sudo dnf install NetworkManager  # Fedora
sudo pacman -S networkmanager    # Arch Linux
```

### Clone the Repository
```sh
git clone https://github.com/Chopan25/python-wifi-manager.git
cd wifi-manager
```

### Install Dependencies
This module relies on Python 3 and `nmcli`. Make sure Python is installed:
```sh
sudo apt install python3
```

### Install Python Package
```sh
python3 setup.py install
```

## Usage Examples

### As a Module
```python
from wifi_manager import WiFiManager

networks = WiFiManager.list_networks()
for net in networks:
    print(net.to_dict())

if networks:
    WiFiManager.connect(networks[0], "your_password")
```
### As a Software
```sh
python3 -m WiFiManager
```
