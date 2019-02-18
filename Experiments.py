from pyo import *
import time
from threading import Thread

s = Server(sr=48000, nchnls=8, buffersize=512, duplex=1).boot()
s.start()


##ind = LinTable([(0,.3), (20,.85), (300,.7), (1000,.5), (8191,.3)])
##m = Metro(4).play()
##tr = TrigEnv(m, table=ind, dur=4)
##f = SumOsc(freq=[301,300], ratio=[.2498,.2503], index=tr, mul=.2).out()
##
##time.sleep(5)
##
##t = SquareTable(order=30).normalize()
##a = Osc(table=t, freq=[100,200], mul=.2).out()
##


lfd = Sine(30, mul=1, add=.5)
a = SuperSaw(freq=[100,50], detune=lfd, bal=0.7, mul=0.2).out()
time.sleep(10)
##path = "/Users/ericlemmon/Google Drive/My Projects/Music Projects/Toy7/Samples/imsend.wav" 
##
##z = True
##
##while True:
##    snd = SndTable(path)
##    end = snd.getSize() - s.getSamplingRate() * 0.2
##    env = HannTable()
##    pos = Randi(min=0, max=1, freq=[1, 0], mul=end)
##    dns = Randi(min=0, max=100, freq=30)
##    pit = Randi(min=.25, max=1.1, freq=100)
##    grn = Granule(snd, env, dens=dns, pitch=pit, pos=pos, dur=.2, mul=.1).out()
##
##    a = input("Type end to End: ")
##
##    if a == "end":
##        break


##
##list1 = [100,200,300,500]
##list2 = [150,250,350,900]
##list3 = [234,5783,463,284]
##
##
##def list_player(list):
##    for i in list:
##        SineTone = Sine(i, 0, 0.1).out()
##        time.sleep(1)
##
##thread1 = Thread(target=list_player, args=[list1])
##thread1.start()
##time.sleep(.33)
##thread2 = Thread(target=list_player, args=[list2])
##thread2.start()
##time.sleep(.05)
##thread3 = Thread(target=list_player, args=[list3])
##thread3.start()
##
##count = 0
##
##while count <= 10:
##    count += 1
##    time.sleep(1)

s.stop()
s.shutdown()
