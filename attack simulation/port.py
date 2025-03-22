import socket

port= int(input("your wanted port :"))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", port))  
s.listen(5)
while True:
    conn, addr = s.accept()