import tkinter as tk
import signal
import time
import os
import subprocess
from tkinter import *
from os import system
from subprocess import check_output
name= check_output(['hostname', '-I'])
name = name.decode()
ip = name
app = tk.Tk()

def kill():
    print("Process {} is closing".format(proc.pid))
    os.kill(proc.pid, signal.SIGTERM)
    tk.messagebox.showinfo( "Stream", "Stream close!")
    newWindow.destroy()

def createNewWindow():
    global newWindow
    newWindow = tk.Toplevel(app)
    labelExample = tk.Label(newWindow, text = "Stream")
    buttonExample = tk.Button(newWindow, text = "Press to stop stream",command = kill)

    labelExample.pack()
    buttonExample.pack()
    newWindow.geometry("300x150")

def Capture():
    #command = 
    tk.messagebox.showinfo( "Capture", "Press 'ok' to capture reference image")
    try:
        # change the location after -o for other USB drives
        cmd = "raspistill -t 10 -n -bm -ex sports -w 648 -h 486 -o /media/pi/disk/Calibrate/Reference.jpg"
            #cmd = "raspistill -t  -ss 5000000 -st -awb off -awbg 2.905,1.91 -w 4056 -h 3040 -o /home/pi/pi8/test/Pi8-%04d.jpg"
        print(cmd)
        p = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(3)
        p.kill()
        tk.messagebox.showinfo( "Capture", "Reference image taken!")
    except Exception as e:
        print(e)
        tk.messagebox.showinfo( "Capture", "Unexpected error!")

def SStream():
    #command = "gst-launch-1.0 -v v4l2src device=/dev/video0 num-buffers=-1 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=192.168.1.66 port=5200"
    #command = "gst-launch-1.0 -v v4l2src device=/dev/video0 num-buffers=-1 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=192.168.50.66 port=5200"
    command = "gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, width=648, height=486, framerate=30/1 ! videoconvert ! autovideosink"
    tk.messagebox.showinfo( "Stream", "Press 'ok' to start streaming")
    try:
        #print(command)
        global proc
        proc = subprocess.Popen(command.split())
        if proc.poll() is None:
            print("Process {} is running".format(proc.pid))
        createNewWindow()
        
    except:
        tk.messagebox.showinfo( "Stream", "Unexpected error!")

def SStreamo():
    #command = "gst-launch-1.0 -v v4l2src device=/dev/video0 num-buffers=-1 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=192.168.1.66 port=5200"
    #command = "gst-launch-1.0 -v v4l2src device=/dev/video0 num-buffers=-1 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=192.168.50.66 port=5200"
    command = "gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, width=648, height=486, framerate=30/1 ! videoconvert ! gdkpixbufoverlay location=/media/pi/disk/Calibrate/Reference.jpg alpha=0.5  ! autovideosink"
    tk.messagebox.showinfo( "Stream", "Press 'ok' to start streaming")
    try:
        #print(command)
        global proc
        proc = subprocess.Popen(command.split())
        if proc.poll() is None:
            print("Process {} is running".format(proc.pid))
        createNewWindow()
        
    except:
        tk.messagebox.showinfo( "Stream", "Unexpected error!")

# def VStream():
#     command = "gst-launch-1.0 -v udpsrc port=5200 ! application/x-rtp, media=video, clock-rate=90000, payload=96 ! rtpjpegdepay ! jpegdec ! videoconvert ! autovideosink"
#     tk.messagebox.showinfo( "Stream", "Press 'ok' to start view streaming")
#     try:
#         system("%s"%command)
#         tk.messagebox.showinfo( "Stream", "Stream close!")
#     except:
#         tk.messagebox.showinfo( "Stream", "Unexpected error!")

print("Ip:{}".format(ip))
B1 = tk.Button(app, text ="Start calibration\nwithout overlay", font=("Times New Roman", 16)
                            , bg='#567', fg='White', command = SStream)
B2 = tk.Button(app, text ="Start calibration\nwith overlay", font=("Times New Roman", 16)
                            , bg='#567', fg='White', command = SStreamo)
B3 = tk.Button(app, text ="Capture reference\nimage for\ncalibration", font=("Times New Roman", 16)
                            , bg='#567', fg='White', command = Capture)
# B4 = tk.Button(app, text ="View stream", font=("Times New Roman", 16)
#                             , bg='#567', fg='White', command = VStream)
B5 = tk.Button(app, text="Exit", font=("Times New Roman", 16)
                            , bg='#567', fg='White', command= app.destroy)

B1.place(x=150,y=10,width=200,height=80)
B2.place(x=150,y=100,width=200,height=80)
B3.place(x=150,y=190,width=200,height=80)
#B4.place(x=150,y=280,width=200,height=80)
B5.place(x=150,y=280,width=200,height=80)
# if(ip =="192.168.50.66"):
#     B1['state'] = tk.DISABLED
#     B2['state'] = tk.DISABLED
#     B3['state'] = tk.NORMAL
#     B4['state'] = tk.NORMAL
# else:
#     B1['state'] = tk.NORMAL
#     B2['state'] = tk.NORMAL
#     B3['state'] = tk.DISABLED
#     B4['state'] = tk.NORMAL
    
if __name__ == "__main__":
    app.geometry("500x450")
    app.title("Calibrate")
    app.option_add('*Dialog.msg.font', 'Helvetica 14')
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
