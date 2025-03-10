from .WiFiManager import WiFiManager as WiFi
import getpass


def main_menu():
    menu_message = '0: Exit\n1: Disconnect from network\n2: List available networks\n3: Connect to a network\n4: Create hotspot'

    print(menu_message)
    selected_option = input('Please select an option to continue: ')
    if selected_option == '0':
        exit()

    elif selected_option == '1':
        WiFi.disconnect()

    elif selected_option == '2':
        networks = WiFi.list_networks()
        list_nets(networks)

    elif selected_option == '3':
        networks = WiFi.list_networks()
        list_nets(networks)
        connect_menu(networks)

    elif selected_option == '4':
        create_hotspot()

    else:
        print('This option is not available, please select a valid option.')


def list_nets(networks):

    table = [['Index', 'In use', 'SSID', 'Signal', 'Security']]
    index = 1
    for network in networks:
        if network.used:
            using = '  YES '
        else:
            using = ''
        table.append([f'  {index}', f'{using}', f'{network.ssid}', f'  {network.signal}', f'{network.security}'])
        index += 1

    for row in table:
        print(f'{row[0]:<5} | {row[1]:<6} | {row[2]:<25} | {row[3]:<6} | {row[4]:<8}')


def connect_menu(networks):
    while True:
        selected_net_index = input('Please enter the index of the Network you want to connect to or 0 to exit: ')

        if selected_net_index == '0':
            return
        elif selected_net_index.isdigit():
            selected_net_index = int(selected_net_index)-1
        else:
            print('This option is not available, please select a valid option.')
            continue

        if selected_net_index < len(networks):
            break
        else:
            print('This option is not available, please select a valid option.')

    if networks[selected_net_index].security != '':
        print('This network has a password.')
        password = getpass.getpass('Please enter the password: ')
        connection_return_code = WiFi.connect(networks[selected_net_index].ssid, password)
    else:
        connection_return_code = WiFi.connect(networks[selected_net_index].ssid)

    if connection_return_code == 0:
        print(f'Successfully connected to {networks[selected_net_index].ssid}')
    else:
        print(print(f'Error connecting to {networks[selected_net_index].ssid}. Please try again.'))


def create_hotspot():
    ssid = input('Ingrese el ssid que desea usar: ')
    password = input('Ingrese la clave para la red: ')
    print(WiFi.create_hotspot(ssid=ssid, password=password))


if __name__ == '__main__':
    print('Welcome to the python network manager package.')
    while True:
        main_menu()
