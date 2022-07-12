import datetime
import logging
import socket
import sys
import time
import subprocess
import os
import utils
import PIL
import glob
import RPi.GPIO as GPIO
import tkinter.messagebox
import tkinter as tk
from tkinter import *
from os import system
from subprocess import check_output
from PIL import Image , ImageFile
from PIL import ImageTk as itk
from utils import get_name, get_ip
from time import process_time
from functools import partial
ImageFile.LOAD_TRUNCATED_IMAGES = True

global start , end
global var
var = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
#get the master ip
name= check_output(['hostname', '-I'])
name = name.decode()
ip = name#.replace(".", "-").strip()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('broadcast')
dest = ('<broadcast>', 5000)

Title_font = ("Times New Roman", 30, "bold")
Button_font = ("Times New Roman", 22)
Button1_font = ("Times New Roman", 18)
Text_font = ("Times New Roman", 14)

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width=1280, height=720)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()
    def end_frame(self ,whole):
#         frame = self.frames[whole]
#         frame.destroy()
        GPIO.cleanup()
        SampleApp.destroy(self)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=1280, height=720)
        # Add image background
        imagebg = (Image.open("camera.png"))
        imagebg = imagebg.resize((1280, 720), Image.ANTIALIAS)
        logo = itk.PhotoImage(imagebg)
        # set image as background
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0, y=0, width=1280, height=720)
        # Create canvas for frame
        canvas1 = Canvas(self, width = 1280, height = 720)
        canvas1.pack(fill = "both", expand = True)
        # Add Image
        canvas1.create_image(0, 0, image = logo, anchor = "nw")
        # Add Text
        canvas1.create_text(640, 40, text = "BulletTime", font=Title_font)
        # Create buttons
        button1 = tk.Button(self, text="Start", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(PageOne))
        button2 = tk.Button(self, text="Help", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(PageTwo))
        button3 = tk.Button(self, text="Exit",font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.end_frame(StartPage))
        button1.place(x=490,y=120,width=300,height=120)
        button2.place(x=490,y=300,width=300,height=120)
        button3.place(x=490,y=480,width=300,height=120)

class PageOne(tk.Frame):    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Add image background
        imagebg = (Image.open("camera.png"))
        imagebg = imagebg.resize((1280, 720), Image.ANTIALIAS)
        logo = itk.PhotoImage(imagebg)
        # set image as background
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=1280,height=720)
        # Create canvas for frame
        canvas1 = Canvas(self, width = 1280, height = 720)
        canvas1.pack(fill = "both", expand = True)
        # Add Image
        canvas1.create_image(0, 0, image = logo, anchor = "nw")
        # Add Text
        canvas1.create_text(640, 40, text = "Menu",font=Title_font)

        def GIF():
            global var
            if(var == False):
                var = True
                if(var == True):
                    try:
                        start = process_time() 
                        for x in range(8):
                            imag = Image.open("/home/pi/Capture/Pi{}-000.jpg".format(x+1))
                            imaggif = imag.resize((1014, 760), Image.ANTIALIAS)
                            imaggif.save("/home/pi/Capture/GIF{}.jpg".format((x+1)))
                        path = 'Bullettime.gif'
                        system('cd Capture&&convert -delay 10 -loop 0 /home/pi/Capture GIF*jpg %s' %path)
                        stop = process_time()
                        tk.messagebox.showinfo('GIF Creation:','GIF created successfully!')
                        time.sleep(0.5)
                        for x in range(8):
                            os.remove("/home/pi/Capture/GIF{}.jpg".format((x+1)))
                        var = False
                        system("pcmanfm \"/home/pi/Capture/%s\"" % path)
                    except:
                        tk.messagebox.showinfo('GIF Creation:','Unexpected error occurred!')
#                     except Exception as e:
#                         print(e)      
            else:
                tk.messagebox.showinfo('GIF Creation:','Unexpected error occurred!')
                
        # Create buttons
        button1 = tk.Button(self, text="Camera Config", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(PageThree))
        button2 = tk.Button(self, text="Display Photo(s)", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(PageFour))
        button3 = tk.Button(self, text="GIF Creattion", font=Button_font
                            , bg='#567', fg='White', command= GIF)
        button4 = tk.Button(self, text="Back", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(StartPage))
        # Display buttons
        button1.place(x=240,y=120,width=300,height=120)
        button2.place(x=740,y=120,width=300,height=120)
        button3.place(x=240,y=480,width=300,height=120)
        button4.place(x=740,y=480,width=300,height=120)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Add image background
        imagebg = (Image.open("camera.png"))
        imagebg = imagebg.resize((1280, 720), Image.ANTIALIAS)
        logo = itk.PhotoImage(imagebg)
        # set image as background
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=1280,height=720)
        # Create canvas for frame
        canvas2 = Canvas(self, width = 1280, height = 720)
        canvas2.pack(fill = "both", expand = True)
        # Add Image
        canvas2.create_image(0, 0, image = logo, anchor = "nw")
        # Add Text
        canvas2.create_text(640, 40, text = "Manual",font=Title_font)
        filename = "/home/pi/Help"
        with open(filename, 'r') as f:
            content = f.read()
        # Create Label
        label = tk.Label(self, text = content , font  = Button1_font , bg = "white")
        # Display Label
        label.place(x=140,y=80,width=1000,height=560)
        # Create buttons
        button1 = tk.Button(self, text="Back", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(StartPage))
        # Display buttons
        button1.place(x=540,y=664,width=200,height=44)

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Add image background
        imagebg = (Image.open("camera.png"))
        imagebg = imagebg.resize((1280, 720), Image.ANTIALIAS)
        logo = itk.PhotoImage(imagebg)
        # set image as background
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=1280,height=720)
        # Create canvas for frame
        canvas3 = Canvas(self, width = 1280, height = 720)
        canvas3.pack(fill = "both", expand = True)
        # Add Image
        canvas3.create_image(0, 0, image = logo, anchor = "nw")
        # Add Text
        canvas3.create_text(640, 40, text = "Select mode", font=Title_font)
        # Create Slider
        qly = tk.IntVar() # Quality
        iso = tk.IntVar() # ISO
        et = tk.DoubleVar() # Exposure time
        wi = tk.IntVar() # width
        he = tk.IntVar() # height
        a = tk.IntVar() # auto
        c = tk.IntVar() # auto
        f = tk.IntVar(value=1) # flash
        rd = tk.DoubleVar() # red gain
        be = tk.DoubleVar() # blue gain
        def QLY_value():
            return '{: }'.format(qly.get())
        def ISO_value():
            return '{: }'.format(iso.get())
        def ET_value():
            return '{: .1f}'.format(et.get())
        def W_value():
            return '{: }'.format(int(wi.get()))
        def H_value():
            return '{: }'.format(int(he.get()))
        def R_value():
            return '{: .2f}'.format(rd.get())
        def B_value():
            return '{: .2f}'.format(be.get())
        def setrb():
            red = r.get()
            blue = b.get()
            if(float(red)<0.00 or float(red)>3.50 or float(blue)<0.00 or float(blue)>3.50):
                rd.set(2.91)
                be.set(1.91)
                Setrb = tk.Toplevel(self,width=400,height=150)
                button = tk.Button(Setrb, text="Exit", font=Button_font
                                    , bg='#567', fg='White', command=Setrb.destroy)
                label = tk.Label(Setrb,text = "Enter a value between \n 0.00 ~ 3.50" , font =Text_font)
                button.place(x=150,y=80,width=100,height=40)
                label.place(x=50,y=30,width=300,height=40)
                valuer_label.configure(text='Red Gain:'+ str(rd.get()))
                valueb_label.configure(text='Blue Gain:'+ str(be.get()))
            else:
                rd.set(red)
                be.set(blue)
                valuer_label.configure(text='Red Gain:'+ str(rd.get()))
                valueb_label.configure(text='Blue Gain:'+ str(be.get()))
        def setw():
            width = w.get()
            if(int(width)<640 or int(width)>4056):
                wi.set(4056)
                Setw = tk.Toplevel(self,width=400,height=150)
                button = tk.Button(Setw, text="Exit", font=Button_font
                                    , bg='#567', fg='White', command=Setw.destroy)
                label = tk.Label(Setw,text = "Enter a value between \n 640 ~ 4056" , font =Text_font)
                button.place(x=150,y=80,width=100,height=40)
                label.place(x=50,y=30,width=300,height=40)
                value3_label.configure(text='Current:'+ str(wi.get()))
            else:
                wi.set(int(width))
                value3_label.configure(text='Current:'+ str(wi.get()))
        def seth():
            height = h.get()
            if(int(height)<480 or int(height)>3040):
                he.set(3040)
                Seth = tk.Toplevel(self,width=400,height=150)
                button = tk.Button(Seth, text="Exit", font=Button_font
                                    , bg='#567', fg='White', command=Seth.destroy)
                label = tk.Label(Seth,text = "Enter a value between \n 480 ~ 3040" , font =Text_font)
                button.place(x=150,y=80,width=100,height=40)
                label.place(x=50,y=30,width=300,height=40)
                value4_label.configure(text='Current:'+ str(he.get()))
            else:
                he.set(int(height))
                value4_label.configure(text='Current:'+ str(he.get()))
        def slider_changed(event):
            value0_label.configure(text='Current:'+QLY_value())
            value1_label.configure(text='Current:'+ISO_value())
            value2_label.configure(text='Current:'+ET_value())
        def SendCommand():
            #send a broadcast message within LAN
            #Send = tk.Toplevel(self,width=400,height=100)
            #button = tk.Button(Send, text="Done", font=Button_font
                            #, bg='#567', fg='White', command=Send.destroy)
            #button.place(x=150,y=60,width=100,height=40)
            global var
            if(var == False):
                var = True
            if(var == True):
                try:
                    # Determine time to take photos
                    now = datetime.datetime.now().replace(microsecond=0)
                    # Add a sync time delay
                    delta = datetime.timedelta(seconds=0)
                    later = now + delta
                    later_iso = later.isoformat()
                    if(a.get()==1):
                        message = 'sync at {}@{}    auto'.format(later_iso,ip.strip('\n'),a.get())
                    else:
                        message = 'sync at {}@{}    expo    {}    {}    {}    {}    {}    {}    {}'.format(later_iso,ip.strip('\n')
                        ,qly.get(),iso.get(),et.get(),wi.get(),he.get(),rd.get(),be.get())
                    b = message.encode()
                    logger.info(later_iso)
                    logger.info(message)
                    for i in range(1):
                        print("Test"+message)
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        s.sendto(message.encode(), dest)

                    tk.messagebox.showinfo('Bullettime:','Configuration sent!')
                    print("auto:{}".format(a.get()))
                    #if(a.get()==0):
                    button1['state'] = tk.DISABLED
                    button2['state'] = tk.NORMAL
                    button3['state'] = tk.DISABLED
                    auto['state'] = tk.DISABLED
                    if(a.get()==0):
                        flash['state'] = tk.NORMAL
                        flash['bg'] = "#567"
                        flash['fg'] = "Yellow"
                    var = False
                except:
                    tk.messagebox.showinfo('Bullettime:','Unexpected error occurred!')
                    var = False
                
        def TakePhoto():
            #send a broadcast message within LAN
            global var
            if(var == False):
                var = True
            if(var == True):
                try:
                    # Determine time to take photos
                    now = datetime.datetime.now().replace(microsecond=0)
                    # Add a sync time delay
                    delta = datetime.timedelta(seconds=0)
                    later = now + delta
                    later_iso = later.isoformat()
                    message = 'sync at {}@{}    take'.format(later_iso,ip.strip('\n'),c.get())
                    b = message.encode()
                    logger.info(later_iso)
                    logger.info(message)
                    for i in range(1):
                        print("Test"+message)
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        s.sendto(message.encode(), dest)
                        noww = datetime.datetime.now()
                        print("sent:{}".format(noww))
                        #time.sleep(0.05)
                        if(a.get()==0):
                            t = et.get()
                            now1 = datetime.datetime.now()
                            #time.sleep(abs(t-1.05)) #for 2nd best option for 3 sec exp, 2.55 is exp 3 sec
                            time.sleep(abs(t-0.5-0.5))
                            GPIO.output(27, GPIO.HIGH) # Buzzer on
                            time.sleep(0.5)
                            GPIO.output(27, GPIO.LOW)
                            GPIO.output(17, GPIO.HIGH)
                            now2 = datetime.datetime.now()
                            print(now2-now1)
                            time.sleep(0.05)
                            GPIO.output(17, GPIO.LOW)
                        if(a.get()==1):
                            GPIO.output(27, GPIO.HIGH) # Buzzer on
                            time.sleep(0.5)
                            GPIO.output(27, GPIO.LOW)
                            time.sleep(5)
#                         else:
#                             GPIO.output(27, GPIO.HIGH) # Buzzer on
#                             #time.sleep(0.45)#0.45)
#                             time.sleep(0.5)
#                             GPIO.output(27, GPIO.LOW)
                    tk.messagebox.showinfo('Bullettime:','Capture images sucessfully!')
                    button1['state'] = tk.NORMAL
                    button2['state'] = tk.DISABLED
                    button3['state'] = tk.NORMAL
                    auto['state'] = tk.NORMAL
                    flash['state'] = tk.DISABLED
                    controller.show_frame(PageFour)
                    var = False
                except:
                    tk.messagebox.showinfo('Bullettime:','Unexpected error occurred!')
                    var = False
        
        # Check box
        auto = tk.Checkbutton(self, text = "Default Setting", font=Button1_font, variable=a)
        auto.place(x=270,y=600,width=200,height=50)
        
        canvas3.create_text(650, 215, text = "Consider a reasonable time if using flash"
                            , font=("Times New Roman", 20),fill="Red")
        flash = tk.Checkbutton(self, text = "Flash", font=Button_font, variable=f)
        flash.place(x=540,y=600,width=200,height=50)
        flash['state'] = tk.DISABLED
        def autocheck():
            global var
            if(var == False):
                var = True
                if(var == True):
                    if(a.get()==1):
                        #print("auto on")
                        slider0.config(state=DISABLED,takefocus=0)
                        slider1.config(state=DISABLED,takefocus=0)
                        slider2.config(state=DISABLED,takefocus=0)
                        buttonw.config(state=DISABLED,takefocus=0)
                        buttonh.config(state=DISABLED,takefocus=0)
                        buttonrb.config(state=DISABLED,takefocus=0)
                        var = False
                    else:
                        #print("auto off")
                        slider0.config(state=NORMAL)
                        slider1.config(state=NORMAL)
                        slider2.config(state=NORMAL)
                        buttonw.config(state=NORMAL)
                        buttonh.config(state=NORMAL)
                        buttonrb.config(state=NORMAL)
                        var = False
            self.after(1000,autocheck)
#         def flashcheck():
#             global var
#             if(var == False):
#                 var = True
#                 if(var == True):
#                     if(f.get()==1):
#                         #print("Flash on")
#                         var = False
#                     else:
#                         #print("Flash off")
#                         var = False
#                     self.after(1000,flashcheck)
        
        #Quality
        slider0 = tk.Scale(self,from_=0,to=100,orient='horizontal',font=Text_font,
                           command=slider_changed,variable=qly)
        slider0.set(100)
        slider0_label = tk.Label(self,text='Quality',font=Text_font)
        value0_label = tk.Label(self,text='Current:'+ QLY_value(),font=Text_font)
        #ISO
        slider1 = tk.Scale(self,from_=100,to=800,orient='horizontal',font=Text_font,
                           command=slider_changed,variable=iso)
        slider1.set(100)
        slider1_label = tk.Label(self,text='ISO',font=Text_font)
        value1_label = tk.Label(self,text='Current:'+ ISO_value(),font=Text_font)
        #Exposure
        slider2 = tk.Scale(self,from_=0,to=60,orient='horizontal',
                           digits = 3, resolution = 0.1 ,font=Text_font,
                           command=slider_changed,variable=et)
        slider2.set(10.0)
        slider2_label = tk.Label(self,text='Shutter Speed',font=Text_font)
        value2_label = tk.Label(self,text='Current:'+ ET_value(),font=Text_font)
        #red and blue
        r = tk.Entry (self,font=("Calibri",16))
        r.insert(0, "2.91")
        b = tk.Entry (self,font=("Calibri",16))
        b.insert(0, "1.91")
        canvas3.create_window(490, 475, width=200, height=50, window=r)
        canvas3.create_window(490, 525, width=200, height=50, window=b)
        buttonrb = tk.Button(self, text="Set", font=Button_font , command=setrb)
        buttonrb.place(x=590,y=475,width=150,height=50)
        r_label = tk.Label(self,text='Red Gain',font=Text_font)
        b_label = tk.Label(self,text='Blue Gain',font=Text_font)
        valuer_label = tk.Label(self,text='Red Gain:'+ R_value(),font=Text_font)
        valueb_label = tk.Label(self,text='Blue Gain:'+ B_value(),font=Text_font)
        #Width
        w = tk.Entry (self,font=("Calibri",16))
        w.insert(0, "4056")
        canvas3.create_window(490, 325, width=200, height=50, window=w)
        buttonw = tk.Button(self, text="Set", font=Button_font , command=setw)
        buttonw.place(x=590,y=300,width=150,height=50)
        w_label = tk.Label(self,text='Width',font=Text_font)
        value3_label = tk.Label(self,text='Current:'+ W_value(),font=Text_font)
        #Height
        h = tk.Entry (self,font=("Calibri",16))
        h.insert(0, "3040")
        canvas3.create_window(490, 375, width=200, height=50, window=h)
        buttonh = tk.Button(self, text="Set", font=Button_font , command=seth)
        buttonh.place(x=590,y=350,width=150,height=50)
        h_label = tk.Label(self,text='Height',font=Text_font)
        value4_label = tk.Label(self,text='Current:'+ H_value(),font=Text_font)
        # Create buttons
        button1 = tk.Button(self, text="Confirm ", font=Button_font
                            , bg='#567', fg='White', command=SendCommand)
        button2 = tk.Button(self, text="Capture ", font=Button_font
                            , bg='#567', fg='White', command=TakePhoto)
        button2.place(x=550,y=600,width=150,height=44)
        button2['state'] = tk.DISABLED
        button3 = tk.Button(self, text="Back", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(PageOne))
        # Display buttons/slider/labels
        button1.place(x=270,y=664,width=200,height=50)
        button2.place(x=540,y=664,width=200,height=50)
        button3.place(x=810,y=664,width=200,height=50)
        slider0_label.place(x=190,y=250,width=150,height=50)
        slider0.place(x=390,y=250,width=500,height=50)
        value0_label.place(x=940,y=250,width=120,height=50)
        slider1_label.place(x=190,y=100,width=150,height=50)
        slider1.place(x=390,y=100,width=500,height=50)
        value1_label.place(x=940,y=100,width=120,height=50)
        slider2_label.place(x=190,y=150,width=150,height=50)
        slider2.place(x=390,y=150,width=500,height=50)
        value2_label.place(x=940,y=150,width=120,height=50)
        r_label.place(x=190,y=450,width=150,height=50)
        valuer_label.place(x=770,y=450,width=120,height=50)
        b_label.place(x=190,y=500,width=150,height=50)
        valueb_label.place(x=770,y=500,width=120,height=50)
        w_label.place(x=190,y=300,width=150,height=50)
        value3_label.place(x=770,y=300,width=120,height=50)
        h_label.place(x=190,y=350,width=150,height=50)
        value4_label.place(x=770,y=350,width=120,height=50)
        self.after(1000,autocheck)
        autocheck()
        #self.after(1000,flashcheck)

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Add image background
        imagebg = (Image.open("camera.png"))
        imagebg = imagebg.resize((1280, 720), Image.ANTIALIAS)
        logo = itk.PhotoImage(imagebg)
        # set image as background
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=1280,height=720)
        # Create canvas for frame
        canvas4 = Canvas( self, width = 1280, height = 720)
        canvas4.pack(fill = "both", expand = True)
        # Add Image
        canvas4.create_image(0, 0, image = logo, anchor = "nw")
        # Add Text
        canvas4.create_text(640, 30, text = "Photo Album", font=Title_font)
        canvas4.create_text(640, 60, text = "(Click the image to enlarge)", font=("Times New Roman", 19))
        
        def enlarge(x):
            a = x
            enlarge = tk.Toplevel(width=1296,height=972)
            enlarge.title("Photo{}".format(a))
            button1 = tk.Button(enlarge, text="Done", font=Button_font
                                , bg='#567', fg='White', command= enlarge.destroy)
            button1.place(x=150,y=60,width=100,height=40)
            imag = Image.open("/home/pi/Capture/Pi{}-000.jpg".format(a))
            imag = imag.resize((1296, 972), Image.ANTIALIAS)
            log = itk.PhotoImage(imag)
            labe = tk.Label(enlarge,image=log)
            labe.image = log
            labe.place(x=0,y=0,width=1296,height=972)
              
        def show():
            global var
            if(var == False):
                var = True
                if(var == True):
                    for x in range(8):
                        #xa=(40+(x*310))
                        imag = Image.open("/home/pi/Capture/Pi{}-000.jpg".format(x+1))
                        imag = imag.resize((250, 200), Image.ANTIALIAS)
                        log = itk.PhotoImage(imag)
                        labe = tk.Label(self,image=log)
                        labe.image = log
                        # Create buttons
                        label = tk.Label(self,text = "Photo{}".format(x+1) , font =Text_font)
                        if(x < 4):
                            xa=(40+(x*310))
                            y = x+1
                            label.place(x=xa,y=80,width=100,height=40)
                            button = tk.Button(self,image =log ,command = lambda y=y: enlarge(y))
                            button.place(x=xa,y=120)
                        else:
                            xa=(40+((x-4)*310))
                            y = x+1
                            label.place(x=xa,y=360,width=100,height=40)
                            button = tk.Button(self,image =log,command = lambda y=y: enlarge(y))
                            button.place(x=xa,y=400)
                    #self.after(3000,show)
                    var = False
        
        def createfile():
            path = "/home/pi/Capture"
            now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            folder = "Capture:{}".format(now)
            print("folder_name: ", folder)
            print("path_name: ", path)
            dirs = os.path.join(path, folder)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
                for x in range(8):
                    imag = Image.open("/home/pi/Capture/Pi{}-000.jpg".format(x+1))
                    imag.save("{}/Pi{}-000.jpg".format(dirs,(x+1)))
                tk.messagebox.showinfo('Bullettime:','Folder created successfully!')
                system("pcmanfm \"%s\"" % dirs)
            else:
                tk.messagebox.showerror('Bullettime','The folder name exists, please change it')
                    
        show()
        button1 = tk.Button(self, text="Refresh\nAlbum", font=Button_font
                            , bg='#567', fg='White', command=lambda:self.after(3000,show))
        button2 = tk.Button(self, text="Save folder\n(with Timestamp)", font=Button_font
                            , bg='#567', fg='White', command=createfile)
        button3 = tk.Button(self, text="Back", font=Button_font
                            , bg='#567', fg='White', command=lambda: controller.show_frame(PageOne))
        # Display button
        button1.place(x=200,y=620,width=200,height=80)
        button2.place(x=520,y=620,width=200,height=80)
        button3.place(x=840,y=620,width=200,height=80)

if __name__ == "__main__":
    app = SampleApp()
    app.geometry("1280x720")
    app.title("Bullettime")
    app.option_add('*Dialog.msg.font', 'Helvetica 14')
    app.resizable(width=False, height=False)
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
