# 5G-network-filter
5G network traffic [code](https://github.com/rlawjd10/5G_udp_socket/blob/main/20240216/server2.py)

## How It Works
1. The script sets up initial `iptables` rules to drop traffic from a specific IP range and allow traffic to a specific IP
2. It reads IP addresses from an `output.json` file and updates `iptables` rules accordingly
3. The script uses `tshark` to monitor network traffic and update the `output.json` file
4. `iptables` rules are dynamically added or removed based on the IP addresses found in `output.json`
