import socket

target_host = "66.241.124.139"
target_port = 514

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data
client.sendto(b"AAABBBCCC", (target_host, target_port))

# Recieve data
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()
