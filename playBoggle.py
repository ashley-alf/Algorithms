from Client import *
from Server import *

if __name__ == "__main__":
    ty = input("Server or Client?")
    ty = ty.lower()
    if ty == "server":
        print("Hello Server")
        addr = input("Enter the IP Address: ")
        port = int(input("Enter the port number: "))
        Server(addr, port)

    if ty == "client":
        print("Hello Client")
        addr = input("Enter the host's IP Address: ")
        port = int(input("Enter the host's port number: "))
        Client(addr, port)
