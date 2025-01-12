# Netscan
This is a simple network scanner based on python programming

# Requirements

First of install requirements using following command.
```
pip install -r requirement.txt
```
# Usage

//For single IP

python netscan.py 192.168.0.1 -p 80 443 -t connect

// you can use single and give range of IPs.

python netscan.py 192.168.0.1 192.168.0.0/24 -p 80 443 -t connect

// Scan important ports

python netscan.py 192.168.0.1 -t connect --imp


