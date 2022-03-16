#!/usr/bin/env python3

# Nick Askam
# Word Generator

import random
import socket
import threading

HEADER = 64
PORT = 5050        # Port to listen on (non-privileged ports are > 1023)
# Run server first to get the IP
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr, words):
    """
    :param words: list of words in the file
    :param conn: connection
    :param addr: address of the connection
    :return: random word
    Get the connection and address and output a random word
    """
    print(f"[NEW CONNECTION] {addr} connected.\n")
    numberOfWords = len(words)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] {msg}")
                conn.send(msg.encode(FORMAT))
            else:
                msg = int(msg)
                print(f"[{addr}]: Printing {msg} words(s)")
                word_to_send = ''
                for x in range(msg):
                    word_index = random.randint(0, numberOfWords - 1)
                    word_to_send += words[word_index] + ' '
                conn.send(word_to_send.encode(FORMAT))


def start(words):
    """
    need the words to run server
    Start the server and add a new thread for the new connection
    :return: an active running server to bring in the words
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, words))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def load_all_words():
    """
    Load in all the words
    :return: a list of the words
    """
    word_file = open('very_long_word_list.txt', 'r')
    valid_words = list(word_file.read().split())
    word_file.close()
    return valid_words


print("[STARTING] server is starting...")
all_words = load_all_words()
start(all_words)



