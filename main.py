print("Hello, World!")


import socket

domain = "google.com"
try:
    ip = socket.gethostbyname(domain)
    print(f"The IP address of {domain} is {ip}")

except socket.gaierror:
    print(f"Could not resolve the domain name: {domain}")