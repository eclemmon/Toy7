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
import random
import threading

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
icq_uh_oh = "/Users/ericlemmon/Google Drive/My Projects/Music Projects/Toy7/Samples/icq.wav"

# ONLY EDIT THESE VALUES, ADD BOUNDARIES AS NEEDED, HAVE FUN WITH DICTIONARIES

lydian_dictionary = {
    0: 440.0000,
    1: 493.8833,
    2: 554.3653,
    3: 622.2540,
    4: 659.2551,
    5: 739.9888,
    6: 830.6094
    }

phrygian_dictionary = {
    0: 329.628,
    1: 349.228,
    2: 391.995,
    3: 440.000,
    4: 493.883,
    5: 523.251,
    6: 587.330
    }

# Classes ARE HERE

class structure_handler(object):
    """
    This class will handle the formal structure of the piece
    """
    def __init__(self, BOUNDARY1, BOUNDARY2, BOUNDARY3, BOUNDARY4, BOUNDARY5, BOUNDARY6, BOUNDARY7):
        self.count = 0
        self.BOUNDARY1 = BOUNDARY1
        self.BOUNDARY2 = BOUNDARY2
        self.BOUNDARY3 = BOUNDARY3
        self.BOUNDARY4 = BOUNDARY4
        self.BOUNDARY5 = BOUNDARY5
        self.BOUNDARY6 = BOUNDARY6
        self.BOUNDARY7 = BOUNDARY7
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
            self.section_one = Section_One(self.count)
            print('section one')
            self.section_one.out()
        elif self.count > 10 and self.count <= self.BOUNDARY1:
            self.transition_one = Transition_One(msg=message.decode("utf-8"), count=self.count)
            print('transition one')
            self.transition_one.out()
        elif self.count > self.BOUNDARY1 and self.count <= self.BOUNDARY2:
            self.section_two = Section_Two(msg=message.decode("utf-8"), count=self.count)
            print('section two')
            self.section_two.out()
        elif self.count > self.BOUNDARY2 and self.count <= self.BOUNDARY3:
            self.transition_two = Transition_Two(msg=message.decode("utf-8"), count=self.count)
            print('transition two')
            self.transition_two.out()
        elif self.count > self.BOUNDARY3 and self.count <=self.BOUNDARY4:
            self.section_three = Section_Three(msg=message.decode("utf-8"), count=self.count)
            print('section three')
            self.section_three.out()
        elif self.count > self.BOUNDARY4 and self.count <= self.BOUNDARY5:
            self.transition_three = Transition_Three(msg=message.decode("utf-8"), count=self.count)
            print('transition three')
            self.transition_three.out()
        elif self.count > self.BOUNDARY5 and self.count <= self.BOUNDARY6:
            self.section_four = Section_Four(msg=message.decode("utf-8"), count=self.count)
            print('section four')
            self.section_four.out()
        elif self.count > self.BOUNDARY6 and self.count <= self.BOUNDARY7:
            self.transition_four = Transition_Four(msg=message.decode("utf-8"), count=self.count)
            print('transition four')
            self.transition_four.out()
        else:
            self.section_five = Section_Five(msg=message.decode("utf-8"), count=self.count)
            print('section five')
            self.section_five.out()
        self.add_to_count()
    def break_point(self):
        self.count = 1000
        self.break_point_piece = break_point_piece()

class break_point_piece(object):
    """
    This class creates a break with a LFO of noise, wooshing around
    """
    def __init__(self):
        self.time_var = 20
        self.fade = pyo.Fader(fadein=0.005, fadeout=10, dur=20).play()
        self.amp = pyo.SigTo(value=self.fade, time=0, init=0.0)
        self.freq = pyo.SigTo(2200, time=7, mul=[1, 1.005], init=2200)
        self.sig = pyo.RCOsc([self.freq, self.freq-20], sharp=4, mul=self.amp).out()
        self.freq.setValue(60)
        self.n = pyo.Noise()
        self.pan_lfo = pyo.Sine(freq=1, mul=.5, add=.5)
        self.fade2 = pyo.Fader(fadein=10, fadeout=10, dur=50).play()
        self.lfo1 = pyo.Sine(freq=.1, mul=500, add=1000)
        self.lfo2 = pyo.Sine(freq=.4).range(2, 8)
        self.bp1 = pyo.ButBP(self.n, freq=self.lfo1, q=self.lfo2, mul=self.fade2)
        self.pan = pyo.SPan(self.bp1, outs=2, pan=self.pan_lfo).out()
        self.fader3 = pyo.Fader(fadein=0.01, fadeout=5, dur=5, mul=3).play()
        self.lfd = pyo.Sine([.4,.3], mul=.2, add=.5)
        self.sawer = pyo.SuperSaw(freq=[49,50], detune=[self.lfd, self.lfd+10], bal=0.7, mul=self.fader3).out()
        time.sleep(50)

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

class Transition_One():
    """
    This class will choose between section one and section two at random and serve as a transition
    """
    def __init__(self, msg, count):
        self.choice = random.random()
        self.message = msg
        self.count = count
        print(self.message)
    def out(self, file_path=imsend_sound_path):
        if self.choice <= 0.33:
            self.section_one = Section_One(self.count)
            self.section_one.out()
        elif self.choice > .33 and self.choice <= .67:
            self.section_two = Section_Two(self.message, self.count)
            self.section_two.out()
        else:
            snd = pyo.SndTable(file_path)
            env = pyo.HannTable()
            pos = pyo.Phasor(snd.getRate()*.25, 0, snd.getSize())
            dur = pyo.Noise(.001, .1)
            g = pyo.Granulator(snd, env, [1, 1.001], pos, dur, 24, mul=1)
            panner = pyo.Pan(g, outs=2, pan=random.random(), spread=random.random()).out()
            time.sleep(2)
            g.stop()
##            print('granulated lol')

class Section_Two(object):
    """
    This class is the second section, it will take in messages and iterate over the characters
    to generate music from them.
    """
    def __init__(self, msg, count):
        self.lydian_list = [lydian_dictionary[ord(letter) % 6] for letter in msg]
        self.phrygian_list = [phrygian_dictionary[ord(letter) % 6] for letter in msg]
        if random.random() <= .5:
            self.message_translation = self.lydian_list
        else:
            self.message_translation = self.phrygian_list
        self.message_length = 5 / len(msg)
        self.octave = 1 + 1/(30 % len(msg)+1)
        self.env = pyo.Fader(fadein=.1, fadeout=.1, dur=0).play()
        if self.octave == 0:
            self.octave = 10
        self.revtime = 0.5
    def out(self):
        choice = random.choice([self.playback1, self.playback2, self.playback3, self.playback4])()

    # Playback Options
    def playback1(self):
        freqs = self.message_translation
        self.env2 = pyo.Fader(fadein=.1, fadeout=1, dur=10.01).play()
        rand = pyo.Choice(choice=freqs, freq=[1,self.message_length])
        osc = pyo.SuperSaw(freq=[rand, rand/2, rand/3], detune=.5, bal=0.8, mul=self.env2).out()
        d = pyo.Delay(osc, delay=[.2, .5, .75], feedback=.5, mul=self.env2)
        panner = pyo.Pan(d, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(self.env2.dur+.001)

    def playback2(self):
        print('pb2')
        fader = pyo.Fader(fadein=0.2, fadeout=0.2, dur=5, mul=.2)
        table = pyo.HarmTable([1,2,2,5,9])
        glissando = pyo.SigTo(value=self.message_translation[0], time=0.1, init=self.message_translation[0])
        osc = pyo.Osc(table=table, freq=[glissando/2, (glissando-1)/2, (glissando+100)/2], mul=fader)
        panner = pyo.Pan(osc, outs=2, pan=random.random(), spread=random.random()).out()
        def pat():
            freq = random.choice(self.message_translation)
            glissando.value = freq
        p = pyo.Pattern(pat, [self.message_length, .25, .75]).play()
        fader.play()
        time.sleep(fader.dur+.05)
        osc.stop()

    def playback3(self, file_path=imsend_sound_path):
        snd = pyo.SndTable(file_path)
        env = pyo.HannTable()
        pos = pyo.Phasor(snd.getRate()*.25, 0, snd.getSize())
        dur = pyo.Noise(.001, .1)
        g = pyo.Granulator(snd, env, [1, 1.001], pos, dur, 24, mul=self.env)
        panner = pyo.Pan(g, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(self.env + 0.05)
        g.stop()

    def playback4(self, file_path=imsend_sound_path):
        select = random.random()
        snd = pyo.SfPlayer(file_path, speed=1, loop=False, mul=5)
        rev = pyo.STRev(snd, inpos=select, revtime=self.revtime, cutoff=5000, bal=1, roomSize=self.revtime)
        panner = pyo.Pan(rev, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(rev.revtime+.01)
        self.revtime += 0.5
        if self.revtime > 3:
            pass
        else:
            self.revtime += 0.5
        time.sleep(self.revtime+.05)
        rev.stop()

class Transition_Two():
    """
    This class will choose between section one and section two at random and serve as a transition
    """
    def __init__(self, msg, count):
        self.message = msg
        self.count = count
        self.selection = random.choice([Section_Two(self.message, self.count), Section_Three(self.message, self.count)])
        print('Section Selected', self.selection)
    def out(self):
        return self.selection.out()

class Section_Three(object):
    """
    This class is the second section, it will take in messages and iterate over the characters
    to generate music from them.
    """
    def __init__(self, msg, count):
        self.lydian_list = [lydian_dictionary[ord(letter) % 6] for letter in msg]
        self.phrygian_list = [phrygian_dictionary[ord(letter) % 6] for letter in msg]
        if random.random() <= .5:
            self.message_translation = self.lydian_list
        else:
            self.message_translation = self.phrygian_list
        self.message_length = 5 / len(msg)
        self.octave = 1 + 1/(30 % len(msg)+1)
        self.env = pyo.Fader(fadein=.1, fadeout=.1, dur=0).play()
        if self.octave == 0:
            self.octave = 10

    def out(self):
        choice = random.choice([self.playback1, self.playback2, self.playback3, self.playback4, self.playback5])()
    
    # Playback Options
    def playback1(self):
        print('pb1')
        freqs = self.message_translation
        self.env2 = pyo.Fader(fadein=.1, fadeout=1, dur=10.01).play()
        rand = pyo.Choice(choice=freqs, freq=[1,self.message_length])
        osc = pyo.SuperSaw(freq=[rand, rand/2, rand/3], detune=.5, bal=0.8, mul=self.env2).out()
        d = pyo.Delay(osc, delay=[.2, .5, .75], feedback=.5, mul=self.env2)
        panner = pyo.Pan(d, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(self.env2.dur+.001)
    
    def playback2(self):
        print('pb2')
        fade = pyo.Fader(fadein=.1, fadeout=0.1, dur = 10).play()
        glissando = pyo.SigTo(value=200, time=0.1, init=200)
        sinewave = pyo.SineLoop(freq=[glissando, glissando*4/5, glissando*4/3], feedback=.1, mul=fade)
        panner = pyo.Pan(sinewave, outs=2, pan=random.random(), spread=random.random()).out()
        def pick_new_freq():
            glissando.value = pyo.Choice(choice=self.message_translation, freq=[1,3])
        pattern = pyo.Pattern(function=pick_new_freq, time=[.25, 1]).play()
        time.sleep(fade.dur + .05)
    
    def playback3(self, file_path=imsend_sound_path):
        print('pb3')
        snd = pyo.SndTable(file_path)
        env = pyo.HannTable()
        pos = pyo.Phasor(snd.getRate()*.25, 0, snd.getSize())
        dur = pyo.Noise(.001, .1)
        g = pyo.Granulator(snd, env, [1, 1.001], pos, dur, 24, mul=self.env)
        panner = pyo.Pan(g, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(2)
        g.stop()
    
    def playback4(self, file_path=imsend_sound_path):
        print('pb4')
        select = random.random()
        snd = pyo.SfPlayer(file_path, speed=1, loop=False, mul=5)
        rev = pyo.STRev(snd, inpos=select, revtime=5, cutoff=5000, bal=1, roomSize=4)
        panner = pyo.Pan(rev, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(rev.revtime+.01)
        rev.stop()
    
    def playback5(self, file_path=icq_uh_oh):
        print('pb5')
        select = random.random()
        snd = pyo.SfPlayer(file_path, speed=1, loop=False, mul=5)
        panner = pyo.Pan(snd, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(1.5)

class Transition_Three():
    """
    This class will choose between section one and section two at random and serve as a transition
    """
    def __init__(self, msg, count):
        self.message = msg
        self.count = count
        self.selection = random.choice([Section_Three(self.message, self.count), Section_Four(self.message, self.count)])
        print('Section Selected', self.selection)
    def out(self):
        return self.selection.out()

class Section_Four(object):
    """
    This class is the second section, it will take in messages and iterate over the characters
    to generate music from them.
    """
    def __init__(self, msg, count):
        self.count = count
        self.lydian_list = [lydian_dictionary[ord(letter) % 6] for letter in msg]
        self.phrygian_list = [phrygian_dictionary[ord(letter) % 6] for letter in msg]
        if random.random() <= .5:
            self.message_translation = self.lydian_list
        else:
            self.message_translation = self.phrygian_list
        self.message_length = 5 / len(msg)
        self.octave = 1 + 1/(30 % len(msg)+1)
        self.env = pyo.Fader(fadein=.1, fadeout=.1, dur=0).play()
        self.granulated_pitch = 1
        if self.octave == 0:
            self.octave = 10

    def out(self):
        choice = random.choice([self.playback1, self.playback2, self.playback3, self.playback4, self.playback5, self.playback5])()
    
    # Playback Options
    def playback1(self):
        print('pb1')
        freqs = self.message_translation
        self.env2 = pyo.Fader(fadein=.1, fadeout=1, dur=10.01).play()
        rand = pyo.Choice(choice=freqs, freq=[1,self.message_length])
        osc = pyo.SuperSaw(freq=[rand, rand/2, rand/3], detune=.5, bal=0.8, mul=self.env2).out()
        d = pyo.Delay(osc, delay=[.2, .5, .75], feedback=.5, mul=self.env2)
        panner = pyo.Pan(d, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(self.env2.dur+.001)
    
    def playback2(self):
        print('pb2')
        fade = pyo.Fader(fadein=.1, fadeout=0.1, dur = 10).play()
        glissando = pyo.SigTo(value=200, time=0.1, init=200)
        sinewave = pyo.SineLoop(freq=[glissando, glissando*4/5, glissando*4/3], feedback=.2, mul=fade)
        panner = pyo.Pan(sinewave, outs=2, pan=random.random(), spread=random.random()).out()
        def pick_new_freq():
            glissando.value = pyo.Choice(choice=self.message_translation, freq=[1,3])
        pattern = pyo.Pattern(function=pick_new_freq, time=[.25, 1]).play()
        time.sleep(fade.dur + .05)
    
    def playback3(self, file_path=imsend_sound_path):
        print('pb3')
        snd = pyo.SndTable(file_path)
        env = pyo.HannTable()
        pos = pyo.Phasor(snd.getRate()*.25, 0, snd.getSize())
        dur = pyo.Noise(.05, .1)
        g = pyo.Granulator(snd, env, [1, 1.001], pos, dur, 24, mul=self.env)
        panner = pyo.Pan(g, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(2)
        g.stop()
    
    def playback4(self, file_path=imsend_sound_path):
        print('pb4')
        select = random.random()
        snd = pyo.SfPlayer(file_path, speed=1, loop=False, mul=5)
        rev = pyo.STRev(snd, inpos=select, revtime=5, cutoff=5000, bal=1, roomSize=4)
        panner = pyo.Pan(rev, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(rev.revtime+.01)
        rev.stop()
    
    def playback5(self, file_path=icq_uh_oh):
        print('pb5')
        count = self.count
        fade = pyo.Fader(fadein=.1, fadeout=0.1, dur = 3).play()
        select = random.random()
        snd = pyo.SndTable(file_path)
        env = pyo.HannTable()
        pos = pyo.Phasor(snd.getRate()*.25, random.random(), snd.getSize())
        dur = pyo.Noise(.05, .1)
        g = pyo.Granulator(snd, env, [self.granulated_pitch, self.granulated_pitch+.001], pos, dur, 24, mul=fade)
        panner = pyo.Pan(g, outs=2, pan=random.random(), spread=random.random()).out()
        self.granulated_pitch -= .05
        if self.granulated_pitch < .049:
            self.granulated_pitch = .05
        time.sleep(fade.dur+.05)
        g.stop()

class Transition_Four():
    """
        This class will choose between section one and section two at random and serve as a transition
        """
    def __init__(self, msg, count):
        self.message = msg
        self.count = count
        self.selection = random.choice([Section_Four(self.message, self.count), Section_Five(self.message, self.count)])
        print('Section Selected', self.selection)
    def out(self):
        return self.selection.out()

class Section_Five(object):
    """
    This class is the second section, it will take in messages and iterate over the characters
    to generate music from them.
    """
    def __init__(self, msg, count):
        self.count = count
        self.lydian_list = [lydian_dictionary[ord(letter) % 6] for letter in msg]
        self.phrygian_list = [phrygian_dictionary[ord(letter) % 6] for letter in msg]
        if random.random() <= .5:
            self.message_translation = self.lydian_list
        else:
            self.message_translation = self.phrygian_list
        self.message_length = 5 / len(msg)
        self.octave = 1 + 1/(30 % len(msg)+1)
        self.env = pyo.Fader(fadein=.1, fadeout=.1, dur=0).play()
        self.granulated_pitch = 1
        if self.octave == 0:
            self.octave = 10

    def out(self):
        choice = random.choice([self.playback1, self.playback2, self.playback3, self.playback4, self.playback5, self.playback5, self.playback5])()
    
    # Playback Options
    def playback1(self):
        print('pb1')
        freqs = self.message_translation
        self.env2 = pyo.Fader(fadein=.1, fadeout=1, dur=10.01).play()
        rand = pyo.Choice(choice=freqs, freq=[1,self.message_length])
        osc = pyo.SuperSaw(freq=[rand, rand/2, rand/3], detune=.5, bal=0.8, mul=self.env2).out()
        d = pyo.Delay(osc, delay=[.2, .5, .75], feedback=.5, mul=self.env2)
        panner = pyo.Pan(d, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(self.env2.dur+.001)
    
    def playback2(self):
        print('pb2')
        fade = pyo.Fader(fadein=.1, fadeout=0.1, dur = 10).play()
        glissando = pyo.SigTo(value=200, time=0.1, init=200)
        sinewave = pyo.SineLoop(freq=[glissando, glissando*4/5, glissando*4/3], feedback=.2, mul=fade)
        panner = pyo.Pan(sinewave, outs=2, pan=random.random(), spread=random.random()).out()
        def pick_new_freq():
            glissando.value = pyo.Choice(choice=self.message_translation, freq=[1,3])
        pattern = pyo.Pattern(function=pick_new_freq, time=[.25, 1]).play()
        time.sleep(fade.dur + .05)
    
    def playback3(self, file_path=imsend_sound_path):
        print('pb3')
        snd = pyo.SndTable(file_path)
        env = pyo.HannTable()
        pos = pyo.Phasor(snd.getRate()*.25, 0, snd.getSize())
        dur = pyo.Noise(.05, .1)
        g = pyo.Granulator(snd, env, [1, 1.001], pos, dur, 24, mul=self.env)
        panner = pyo.Pan(g, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(2)
        g.stop()
    
    def playback4(self, file_path=imsend_sound_path):
        print('pb4')
        select = random.random()
        snd = pyo.SfPlayer(file_path, speed=1, loop=False, mul=5)
        rev = pyo.STRev(snd, inpos=select, revtime=4, cutoff=5000, bal=1, roomSize=4)
        panner = pyo.Pan(rev, outs=2, pan=random.random(), spread=random.random()).out()
        time.sleep(rev.revtime+.01)
        rev.stop()
    
    def playback5(self, file_path=icq_uh_oh):
        print('pb5')
        count = self.count
        fade = pyo.Fader(fadein=.1, fadeout=0.1, dur = 3).play()
        select = random.random()
        snd = pyo.SndTable(file_path)
        env = pyo.HannTable()
        pos = pyo.Phasor(snd.getRate()*.25, random.random(), snd.getSize())
        dur = pyo.Noise(.05, .1)
        g = pyo.Granulator(snd, env, [self.granulated_pitch, self.granulated_pitch+.001], pos, dur, 24, mul=fade)
        panner = pyo.Pan(g, outs=2, pan=random.random(), spread=random.random()).out()
        self.granulated_pitch -= .05
        if self.granulated_pitch < .049:
            self.granulated_pitch = .05
        time.sleep(fade.dur+.05)
        g.stop()

    def playback6(self):
        print('pb6')
        self.time_var = 20
        self.fade = pyo.Fader(fadein=0.005, fadeout=10, dur=20).play()
        self.amp = pyo.SigTo(value=self.fade, time=0, init=0.0)
        self.freq = pyo.SigTo(2200, time=7, mul=[1, 1.005], init=2200)
        self.sig = pyo.RCOsc([self.freq, self.freq-20], sharp=4, mul=self.amp)
        panner = pyo.Pan(self.sig, outs=2, pan=random.random(), spread=random.random()).out()


if __name__ == "__main__":
    structure = structure_handler(10, 20, 30, 40, 50, 60, 70)
    client_enter_test = client_enters_chat()
    client_leave_test = client_leaves_chat()
    client_message_test = Section_One(5)
    section_two_test1 = Section_Two('asdfasdf', 24)
    transition_one_test1 = Transition_One('asdjfjsdfhasjkhas', 25)
    transition_one_test2 = Transition_One('kjsadbfjkbsdjksdajkvbjksdbbvkds', 25)
    transition_one_test3 = Transition_One('aaskjdbvkjbsdvjkbdksjbvkjbasdkjvbkjds', 25)
    transition_two_test1 = Transition_Two('aksjdkadsbkdsfasd', 50)
    transition_two_test2 = Transition_Two('%$E$%D^%CGHVYUIO*FVHJVJBVJV', 50)
    transition_two_test3 = Transition_Two('ab', 50)
    section_two_test2 = Section_Two('@#$%$D◊‡°‡ˇ◊˝ÎÁˇ‰Íﬂ‡ÔÓ◊ı, THE GREAT BLONG WHITE the great blong white, LONG TEXT LOL,', 24)
    section_three_test1 = Section_Three('@#$%$D◊‡°‡ˇ◊˝ÎÁˇ‰Íﬂ‡ÔÓ◊ı, THE GREAT BLONG WHITE the great blong white, LONG TEXT LOL,', 24)
    section_three_test2 = Section_Three('asdfasdf', 24)
    section_four_test1 = Section_Four('@#$%$D◊‡°‡ˇ◊˝ÎÁˇ‰Íﬂ‡ÔÓ◊ı, THE GREAT BLONG WHITE the great blong white, LONG TEXT LOL,', 24)
    section_four_test2 = Section_Four('asdfasdf', 24)
    transition_three_test = Transition_Three('asdghsghtrhrth', 50)
    transition_four_test = Transition_Four('asdhdsjdhjd', 50)
    section_five_test = Section_Five('sadfgdfgdfasgfes', 60)

    test_list = [section_two_test1, transition_one_test1, transition_two_test1, section_three_test1, section_four_test1, transition_three_test, transition_four_test, section_five_test]
    
    for i in test_list:
        try:
            i.playback1()
            i.playback2()
            i.playback3()
            i.playback4()
            i.playback6()
            i.playback5()
            i.out()
        except:
            print(i)
            print('passing')
            pass
    

    
    sound_server.stop()
    sound_server.shutdown()

    
