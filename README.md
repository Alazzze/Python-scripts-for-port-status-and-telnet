# Python Scripts for Port Status and Telnet Interaction

## Check Port Status Script

### Description
This script allows you to check if a specified port on a host is open or to wait for it to become available within a given timeout.

### Usage
```bash
python check_port_status.py --address <host_address> --port <port_number> --timeout <max_wait_timeout>

Arguments
--address: Host address
--port: Port number
--timeout: Maximum wait timeout in seconds (default: 15)

**Examples**
Check if a port is open:
python check_port_status.py --address 127.0.0.1 --port 22
Wait for a port to become available:
python check_port_status.py --address example.com --port 80 --timeout 30



Telnet Interaction Script
Description
This script allows you to interact with a switch using the Telnet protocol. It supports receiving data from the switch, sending commands, and checking the status of a specified port.

Usage
python telnet_interaction.py --address <switch_ip> --port <switch_port>
Arguments
--address: Switch IP address
--port: Switch port

Examples
Connect to a switch and interactively send commands:
python telnet_interaction.py --address 192.168.1.1 --port 23

Check the status of a specific port on the switch:
python telnet_interaction.py --address 192.168.1.1 --port 22

Feel free to customize this README based on your specific needs. You can add more details, examples, or any additional information you find relevant.


