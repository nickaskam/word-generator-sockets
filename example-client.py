#!/usr/bin/env python3

# Nick Askam
# Example client

import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.86.152'  # Run server first
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

list_of_words = []


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    word_received = client.recv(2048).decode(FORMAT)
    if word_received != DISCONNECT_MESSAGE:
        temp_list = word_received.split()
        for word in temp_list:
            list_of_words.append(word)


# Send the number of words that you would like back
send("5")
send(DISCONNECT_MESSAGE)
print(list_of_words)
