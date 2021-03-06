#!/usr/bin/python2.7
#
# Author: LukeBob
#
# Requires the pip instilation of Twilio. ==> (pip install twilio)
#
# If you want to use the text function you will have to make a free account at https://www.twilio.com .

import datetime
import hashlib
import socket
import time
from twilio.rest import TwilioRestClient
import subprocess
import sys, traceback
from Crypto.Cipher import AES
import readline

now = datetime.datetime.now().strftime("%d/%m/%y  %H-%M")
accountSid = '' # Account sid
authToken = ''  # Account auth token
key32 = hashlib.sha256("test password").digest()[:256] # Your secret password, Shared with the client
    

def iptables(person):
    subprocess.call('/sbin/iptables -I INPUT -s '+person+' -j DROP',shell=True)

def Main():
    try:
        trusted = ['127.0.0.1'] # trusted ip list
        host = '127.0.0.1'      # server host
        port = 50098            # server port
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)
        c, addr = s.accept()
        person = str(addr)
        person = person[1:-8]
        person = person.replace("'",'',2)
        if person not in trusted:
            print '\nFailed Connection Occurance...\n'
            time.slpeep(1)
            iptables(person)    # Any ip not trusted list gets banned
            time.sleep(1)
            print 'Banned '+person+' with iptables!..'

        while True:
            data = c.recv(1024)

            if not data:
                break

            if len(data) == 16:
                iv = data
                data = "New Iv Recived.."
                subprocess.call('echo '+data+' >> test.txt', shell=True)
            else:
                obj2 = AES.new(key32, AES.MODE_CFB, iv)
                data1 = obj2.decrypt(data)
                alldata = 'Data: '+data1+' -  Host: '+person+'  -  Time: '+now
                client = TwilioRestClient(accountSid, authToken)
                client.messages.create( body=data1, to='Your Mobile Num', from_=,'Twilio Phone Num'>)
                subprocess.call('echo '+alldata+' >> test.txt', shell=True)
                time.sleep(300)  # Message delay
                                
        c.close()
    except KeyboardInterrupt:
        print ("Exiting...")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == '__main__':
    Main()
