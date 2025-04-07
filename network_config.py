from netmiko import ConnectHandler
# ConnectHandler allows for SSH connections to the network devices

# Create a python dictionary with will contain the necessary details to connect to the device
# if we're connecting to multiple devices, make multiple dictionaries
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',  # Router IP address
    'username': 'admin',  # SSH username
    'password': 'your_password',  # SSH password
    'secret': 'enable_password',
    'port': 22,
}
# Connection is a variable that stores the "ConnectHandler" function
# it will unpack the dictionary(ies) and establish the connection(s)

ssh = ConnectHandler(**device)


# if connecting to multiple devices use this;
# for device in (device1, device2, device3... device#:
#    net_connect = ConnectHandler(**device)

   # This allows the device to enter "enabled" mode, which will allow us to perform
                        # the certian configuration tasks for said device(s)
                        #if the device requires an password, it'll be used here

# Below is a list which will perform the config commands specified inside and will apply to said device(s)
config_commands = [
    'interface FastEthernet0/0',
    'ip address 192.168.1.1 255.255.255.0',  # Update the IP address if needed
    'no shutdown',  # Ensure interface is up
    'ip routing',
]

# This will send the list, "config_commands" to the device through the established SSH session
# using ".send_config_set" will send multiple commands at once to the device and waits for the output
# the "output" variable will capture the response and store it
output = ssh.send_config_set(config_commands)

# Will print out the result of the command execution returned by
# the device whether it be a success, failure, error, or the results of the commands
print(output)

# This will disconnect the session
ssh.disconnect()

