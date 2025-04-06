from netmiko import ConnectHandler

device = {
    'device_type': '',
    'host': '192.168.56.101',
    'username': '',
    'password': '',
    'secret': '',
}

connection = ConnectHandler(**device)
connection.enable()