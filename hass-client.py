#!/usr/bin/env python

import os
import sys
import getopt
from time import sleep
from espeak import espeak
import RPi.GPIO as GPIO
from sseclient import SSEClient
import json
from datetime import datetime

microphoneGPIO = 26
debug=False
volume=100
GPIO.setmode(GPIO.BCM)
GPIO.setup(microphoneGPIO, GPIO.OUT)

es=espeak
es.set_voice('en-us')
#es.set_parameter(es.Parameter.Pitch,60)
# es.set_parameter(es.Parameter.Range,60)
#es.set_parameter(es.Parameter.Rate,150)
es.set_parameter(es.Parameter.Wordgap,4)

def main(argv):
    words = ''
    print 'Argument List:', str(argv)
    speak(argv)


def speak(words):
    GPIO.output(microphoneGPIO, True)
    sleep(1)
    es.synth("Simon Says, " + str(words))
    while (es.is_playing()):
        sleep(.1)
    GPIO.output(microphoneGPIO, False)


if __name__ == "__main__":
    # Set Volume
    os.system("amixer set PCM -- " + str(volume) + "%")
    if sys.argv[1:]:
        main(sys.argv[1:])
        sys.exit(0)

    while(1):
        messages = SSEClient('http://home-assitant-server.local:8123/api/stream?api_password=abc1234')
        for msg in messages:
            #
            # print(parsed_json)
            sleep(1)
            if(str(msg)!="ping"):
                parsed_json = json.loads(str(msg))

                # Check if it was the front door lock
                try:
                    if(parsed_json['data']['topic']=='smartthings/FrontDoor/lock'):
                        if (parsed_json['data']['payload']=='unlocked'):
                            sleep(90)
                            print("Welcome home!")
                            speak("Welcome home!")
                        if (parsed_json['data']['payload']=='locked'):
                            speak("Have a good day!")
                except:
                    pass

                # Check if it was the front door lock
                try:
                    if (parsed_json['data']['topic'] == 'smartthings/Bar Lights/switch'):
                        if (parsed_json['data']['payload'] == 'on'):
                            print("Shall I make you a cocktail too?")
                            speak(", Should I make you, a cocktail?")
                        if (parsed_json['data']['payload'] == 'off'):
                            speak("Party time is over")
                except:
                    pass

                if(debug):
                    print(parsed_json)
                    # print("MSG: -" + str(msg) +"-")
