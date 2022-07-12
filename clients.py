#!/usr/bin/env python
# original code from:
# http://www.prodigyproductionsllc.com/articles/programming/write-a-udp-client-and-server-with-python/
import datetime
import logging
import re
import socket
import sys
import time
import os
import signal
import subprocess
#from os import system

SYNC_RE = re.compile(r'sync at (?P<timestamp>.*)@')

#fn = ("PiClient-%s.jpg" %ip)
fn = ("/home/pi/pi2/Pi2-%03d.jpg")

global start ,start1
global end, end1
global receiveip ,cmd ,cmd1
global proc , proc1
global exps
count =0

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('listener')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', 5000))

logger.info('Listening for broadcasts...')

def download():
    #send picture to master with ssh
    process = subprocess.Popen(
#         ("scp Pi1-0000.jpg pi@172.20.10.2:/home/pi/Capture").split() #Mobile hotspot ip
        ("scp -r /home/pi/pi2/Pi2-000.jpg pi@{}:/home/pi/Capture".format(receiveip).split()  #ip received
    ))
    process.wait()

while True:
    try:
        global start,end,proc,cmd,cmd1,exps
        answer = s.recvfrom(8192)
        #decide and match to ensure its from master
        start = time.time()
        matches = SYNC_RE.match(answer[0].decode())
        msg = answer[0].decode()
        print(msg)
        if not matches:
            print('No match!')
            continue
        receiveip = msg[28:43]
        receiveip = receiveip.strip()
        print(msg[43:50].strip())
        if(msg[43:50].strip() =="auto"):
            global cmd
            print("auto mode")
            cmd = "raspistill -t 0 -s -bm -ex sports -o /home/pi/pi2/Pi2-000.jpg"
             #cmd = "raspistill -t 0 -s -md 3 -n -bm -ex off -ag 1 -q 100 -ISO 800 -ss 5000000 -st -awb off -awbg 2.905,1.91 -w 4056 -h 3040 -o /home/pi/pi8/test/Pi8-%04d.jpg"
            print(cmd)
            count = 1 
            proc = subprocess.Popen(cmd.split())
            time.sleep(3)
            #proc.wait()
        if(msg[43:50].strip() =="expo"):
            global cmd1
            print("expo mode")
            ql = msg[50:58].strip()
            iso = msg[58:65].strip()
            exp = float(msg[65:72].strip())
            exp = str(int(exp*1000000))
            exps = exp
            w = int(msg[72:80].strip())
            h = int(msg[80:88].strip())
            rg = float(msg[88:96].strip())
            bg = float(msg[96:].strip())
            #cmd1 = "raspistill -t 0 -s -md 3 -n -bm -ex off -ag 1 -q {} -ISO {} -st -awb off -awbg 2.905,1.91 -w {} -h {} -o /home/pi/pi8/test/Pi8-000.jpg".format(ql,iso,w,h)
            #cmd1 = "raspistill -t 1 -s -md 3 -n -bm -ex off -ag 1 -q 100 -ISO 800 -ss 2000000 -st -awb off -awbg 2.905,1.91 -w 4056 -h 3040 -o /home/pi/pi8/test/Pi8-000.jpg"
            cmd1 = "/usr/bin/raspistill -t 0 -s -md 3 -n -bm -ex off -ag 1 -ss {} -q {} -ISO {} -st -awb off -awbg {},{} -w {} -h {} -o /home/pi/pi2/Pi2-000.jpg".format(exp,ql,iso,rg,bg,w,h)
            print(cmd1)
            proc = subprocess.Popen(cmd1.split(), shell = False)
            if proc.poll() is None:
                print("Process {} is running".format(proc.pid))
        if(msg[43:50].strip() =="take"):
            #if proc.poll() is None:
            print("taking photo")
            print("Proc:{}".format(proc.pid))
#                 #proc.send_signal(signal.SIGUSR1)
            os.kill(proc.pid, signal.SIGUSR1)
#             #proc.send_signal(signal.SIGUSR1)
#             #os.system("pkill -USR1 raspistill")
            home_dir = "help"
            print("ran with exit code {}".format(home_dir))
# #                 cmd2 ="pkill -USR1 raspistill"
#                 proc2 = subprocess.Popen(cmd2.split())
            if count == 1:
                print("count auto")
                time.sleep(5)
                count = 0
            else:
                print("count manual")
                expt = (float(exps)/1000000) + 1
                print(expt)
                time.sleep(expt)
            proc.terminate()
            print("photo taking process complete")
            download()
    except (KeyboardInterrupt, SystemExit):
        break
    except Exception as e:
        logger.exception(e)
