#!/usr/bin/env python3

"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from Music_Handler import *
import pyo
import time


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the chat! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    # Insert client enters chat function here
    enter_sound = client_enters_chat()
    enter_sound.out()
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
            #insert formal function class here, and begin calling methods
            TOY7_STRUCTURE.structure(msg)    
        else:
            client.send(bytes("{quit}", "utf8"))
            exit_sound = client_leaves_chat()
            exit_sound.out()
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            time.sleep(1)
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


""" BELOW HERE are the global variables """     
clients = {}
addresses = {}
BOUNDARY1 = 50
BOUNDARY2 = 100

""" Set only HOST and PORT according to your wifi/lan + Client settings"""

HOST = '192.168.1.9'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    #Start formal structure here
    TOY7_STRUCTURE = structure_handler(BOUNDARY1, BOUNDARY2)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
