#!/usr/bin/env python3

"""
This Module serves as a collection of functions
(and maybe classes) that will take in the text
from clients and convert them to music based on
the portion of the piece that we are in.
"""
# Imports
import pyo
import time

# Boot sound synthesis server
sound_server = pyo.Server(sr=48000, nchnls=8, buffersize=512, duplex=1).boot()
sound_server.start()

# GLOBALS ARE HERE
# The count sets the number of messages counted to 0
# so as to track the number of messages and iterate through
# methods that represent different sections.
# Set the boundaries to larger or smaller numbers based
# on how long you want to chat/make music for.

# DO NOT EDIT THESE PATHS OR VALUES
count = 0

# Sound sample file paths
imsend_sound_path = "/Users/ericlemmon/Google Drive/My Projects/Music Projects/Toy7/Samples/imsend.wav"
imrcv_sound_path = "/Users/ericlemmon/Google Drive/My Projects/Music Projects/Toy7/Samples/imrcv.wav"
enter_sound_path = "/Users/ericlemmon/Google Drive/My Projects/Music Projects/Toy7/Samples/buddyin.wav"
exit_sound_path = "/Users/ericlemmon/Google Drive/My Projects/Music Projects/Toy7/Samples/buddyout.wav"

# ONLY EDIT THESE VALUES, ADD BOUNDARIES AS NEEDED, HAVE FUN WITH DICTIONARIES
BOUNDARY1 = 50
BOUNDARY2 = 100

lydian_dictionary = {
    0: 440.0000,
    1: 493.8833,
    2: 554.3653,
    3: 622.2540,
    4: 659.2551,
    5: 739.9888,
    6: 830.6094
    }

# Classes ARE HERE

class structure_handler(object):
    def __init__(self, BOUNDARY1, BOUNDARY2):
        self.count = 0
        self.BOUNDARY1 = BOUNDARY1
        self.BOUNDARY2 = BOUNDARY2
        print('Starting formal structure...')
    def get_message(self):
        return self.message
    def get_count(self):
        return self.count
    def set_message(self, msg):
        self.message = msg
    def add_to_count(self):
        self.count += 1
        print(self.count)
    def structure(self, message):
        if self.count <= 10:
            self.client_message = Section_One(self.count)
            print('playing message sound')
            self.client_message.out()
            self.add_to_count()
        elif self.count > 10 and self.count <= self.BOUNDARY1:
            self.section_two = Section_Two(msg=str(message), count=self.count)
            self.section_two.out()
            self.add_to_count()
        elif self.count > self.BOUNDARY1 and self.count < self.BOUNDARY2:
            self.section_three(msg)

class client_enters_chat(object):
    """
    This function checks the count and performs more or less granular synthesis
    on the audio file based on where the count is
    """
    def __init__(self):
        self.client_entered = pyo.SfPlayer(enter_sound_path, speed=[1, 0.995], loop=False, mul=0.4)
    def out(self):
        self.client_entered.out()

class client_leaves_chat(object):
    """
    This class checks the count and performs more or less granular synthesis
    on the audio file based on where the count is
    """
    def __init__(self):
        self.client_left = pyo.SfPlayer(exit_sound_path, speed=[1, 0.995], loop=False, mul=0.4)
    def out(self):
        self.client_left.out()

class Section_One(object):
    """
    This class is the first section, and just returns the standard AIM 'ping' sound
    when a message is recieved by the server.
    """
    def __init__(self, count):
        self.even_odd = count
        self.client_messaged_even = pyo.SfPlayer(imsend_sound_path, speed=[1, 0.995], loop=False, mul=0.4)
        self.client_messaged_odd = pyo.SfPlayer(imrcv_sound_path, speed=[1, 0.995], loop=False, mul=0.4)
    def out(self):
        if self.even_odd % 2 == 0:
            self.client_messaged_even.out()
            self.even_odd += 1
        else:
            self.client_messaged_odd.out()
            self.even_odd += 1
        print('even_odd is: ', self.even_odd)

class Section_Two(object):
    """
    This class is the second section, it will take in messages and iterate over the characters
    to generate music from them.
    """
    def __init__(self, msg, count):
        self.message_translation = [lydian_dictionary[ord(letter) % 6] for letter in msg]
        self.message_length = 5 / len(msg)
        self.octave = (40 % len(msg))
        if self.octave == 0:
            self.octave = 10
    def out(self):
        for number in self.message_translation:
            self.SineTone = pyo.Sine((number/2), mul=self.message_length, add=0.5)
            play_out = pyo.SuperSaw(freq=[number/self.octave, number/self.octave], detune=self.SineTone, bal=0.7, mul=0.2).out()
            time.sleep(1 * self.message_length)
        self.SineTone.stop()
        
    
    
if __name__ == "__main__":
    
    client_enter_test = client_enters_chat()
    client_leave_test = client_leaves_chat()
    client_message_test = Section_One()
    section_two_test = Section_Two(input('type something here: '))

    test_list = [client_enter_test, client_leave_test, client_message_test, client_message_test, section_two_test]

    for i in test_list:
        i.out()
        time.sleep(1)
    
    while input('type "stop" to stop: ').lower() != 'stop':
        pass
    sound_server.stop()
    sound_server.shutdown()

    
