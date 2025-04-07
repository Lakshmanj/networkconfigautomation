from netmiko import ConnectHandler
# ConnectHandler allows for SSH connections to the network devices

# Create a python dictionary that will contain the necessary details to connect to the device
# if we're connecting to multiple devices, make multiple dictionaries
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',  # Router IP address
    'username': 'admin',  # SSH username
    'password': 'your_password',  # SSH password
    'port': 22,          # This is the port number for SSH, default is 22
    'secret': 'enable_password',  # This is the enable password for the device, if required
}
# Connection is a variable that stores the "ConnectHandler" function
# it will unpack the dictionary(ies) and establish the connection(s)

try:
    ssh = ConnectHandler(**device)
    # This allows the device to enter "enabled" mode, which will allow us to perform
    # certain configuration tasks for said device(s)
    ssh.enable()
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

# Below is a list that will perform the config commands specified inside and will apply to said device(s)
config_commands = [
    # Basic interface setup
    'interface FastEthernet0/0',
    'ip address 192.168.211.2 255.255.255.0',  # Update the IP address to match the host's subnet
    'no shutdown',  # Ensure interface is up

    # SSH configuration for secure remote management
    'hostname Router1',  # Sets the router name
    'ip domain-name example.com',  # Configures a domain name
    'crypto key generate rsa modulus 1024',  # Generates RSA keys for SSH
    'ip ssh version 2',  # Uses the more secure SSH version 2
    'username admin privilege 15 secret your_password',  # Creates a privileged user
    'line vty 0 4',  # Configures virtual terminal lines
    'transport input ssh',  # Enables SSH input
    'login local',  # Requires local authentication for SSH

    # SNMP setup for monitoring network devices
    'snmp-server community public RO',  # Configures a read-only SNMP community string
    'snmp-server location Toronto',  # Specifies device location
    'snmp-server contact admin@example.com',  # Adds contact info

    # Dynamic routing protocol configuration (OSPF)
    'router ospf 1',  # Starts OSPF process with ID 1
    'network 192.168.211.0 0.0.0.255 area 0',  # Defines OSPF network range and area

    # Basic security measures
    'interface FastEthernet0/1',
    'shutdown',  # Shuts down unused interfaces
    'access-list 10 permit 192.168.211.0 0.0.0.255',  # ACL allowing specific subnet
    'line vty 0 4',
    'access-class 10 in',  # Restricts access to specific hosts

    # Logging setup for troubleshooting
    'logging buffered 10000',  # Enables log buffering
    'service timestamps log datetime',  # Adds timestamps to logs
]

try:
    # This will send the list, "config_commands," to the device through the established SSH session
    # using ".send_config_set" will send multiple commands at once to the device and waits for the output
    # the "output" variable will capture the response and store it
    output = ssh.send_config_set(config_commands)
    print(output)  # Will print out the result of the command execution returned by the device
    # Save logs to a file for reference and troubleshooting
    with open("config_log.txt", "w") as log_file:
        log_file.write(output)
except Exception as e:
    print(f"Configuration failed: {e}")
finally:
    print("Closing connection...")
    # This will disconnect the session
    ssh.disconnect()
    print("Connection closed.")
# This script configures a Cisco router using SSH and Netmiko, applying basic settings, security measures, and logging.