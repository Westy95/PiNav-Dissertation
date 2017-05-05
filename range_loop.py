#!/usr/bin/python
#import libraries
import RPi.GPIO as GPIO
import time
import pyglet
import sys
from Tkinter import *
import tkFont

win = Tk()
win.title("Parking Sensor")
win.geometry('900x450')


myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')


def exitProgram():
    print("Exit Button pressed")
    keepGoing = False
    GPIO.cleanup()
    win.quit()
    
canvas = Canvas(width=900, height=300, bg='white')
canvas.pack(expand=YES, fill=BOTH)

label = Label(canvas, height=3, anchor=CENTER, fg='white', bg='black')
label.pack()

exitButton = Button(win, text = "Exit", font = myFont, command = exitProgram, height = 2, width = 6)
exitButton.pack(side = BOTTOM)

#set GPIO mode
GPIO.setmode(GPIO.BCM)

music = pyglet.resource.media('ball.wav',streaming=False)

#set GPIO pins
TRIG = 23
ECHO = 24

print "Distance Measurement in Progress..."

#set GPIO direction (in/out)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    #set trig to high
    GPIO.output(TRIG, True)

    #set trig to low after 0.01ms
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    StartTime = time.time()
    EndTime = time.time()

    #save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    #save time of arrival
    while GPIO.input(ECHO) == 1:
        EndTime = time.time()

    #time difference between start and arrival 
    TimeElapsed = EndTime - StartTime 

    #multiply with sonic speed
    distance = TimeElapsed * 17150

    return distance

keepGoing = True

if __name__ == '__main__':
    try:
        while keepGoing:
            win.update()
            dist =distance()
            label.config(text="%.1f"%dist)
            label.config(font=("Courier", 32))
            if dist <= 2:
                print "Distance", dist, "cm"
                canvas.create_rectangle(0, 0, 900, 500, width=5, fill='red')
                music.play()
                time.sleep(0.001)
                
            elif dist >= 2 and dist <= 5:
                print "Distance", dist, "cm"
                canvas.create_rectangle(0, 0, 900, 500, width=5, fill='red')
                music.play()
                time.sleep(0.1)

            elif dist >= 5 and dist <= 10:
                print "Distance", dist, "cm"
                canvas.create_rectangle(0, 0, 900, 500, width=5, fill='red')
                music.play()
                time.sleep(0.2)
                
            elif dist >= 10 and dist <= 20:
                print "Distance", dist, "cm"
                canvas.create_rectangle(0, 0, 900, 500, width=5, fill='yellow')
                music.play()
                time.sleep(0.3)
            elif dist >= 20 and dist <= 40:
                print "Distance", dist, "cm"
                canvas.create_rectangle(0, 0, 900, 500, width=5, fill='yellow')
                music.play()
                time.sleep(0.6)
            else:
                print "Distance", dist, "cm"
                canvas.create_rectangle(0, 0, 900, 500, width=5, fill='green')
                music.play()
                time.sleep(1)

    except KeyboardInterrupt:
        print "Measurement stopped by User"
        GPIO.cleanup()
#win.mainloop()
