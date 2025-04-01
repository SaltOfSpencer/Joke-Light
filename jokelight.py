from __future__ import print_function
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sid_obj = SentimentIntensityAnalyzer()
import cv2
import os
import subprocess
import cv2 as cv
from mss import mss
from PIL import Image
import numpy as np
import argparse
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from winsound import *
from tkinter import filedialog
import sys
import shutil
LARGEFONT = ("Verdana", 35)

#whisper_installation="python -m pip install git+https://github.com/openai/whisper.git"
#os.system(whisper_installation)

model = YOLO("best.pt")
global userid
global faces
global tags
global filename
bool = False
face_cascade_name = "C:\\Users\\Annabelle Cheverton\\PycharmProjects\\Popup\\.venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml"  # args.face_cascade
eyes_cascade_name = "C:\\Users\\Annabelle Cheverton\\PycharmProjects\\Popup\\.venv\\Lib\\site-packages\\cv2\\data\\haarcascade_eye_tree_eyeglasses.xml"  # args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)
def browsercallback():
    global buttonClick
    buttonClick = not buttonClick
buttonClick = False


def detectAndDisplay(screen,framename):
    classlist = []


    screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    screen_gray = cv.equalizeHist(screen_gray)
    faces = face_cascade.detectMultiScale(screen_gray)
    if any(map(len, faces)):
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        frame = screen.copy()
        dim = min(w,h)
        frame = frame[y:y + dim, x:x + dim]
        if dim != 48:
            if dim < 48:
                frame = cv.resize(frame, (48, 48), interpolation=cv.INTER_LINEAR)
            else:
                frame = cv.resize(frame, (48, 48), interpolation=cv.INTER_AREA)

        frame = cv.resize(frame, (48, 48), interpolation=cv.INTER_LINEAR)
        print (framename)
        results = model(frame)
        r = results[0]
        classes = r.boxes.cls.tolist()
        for g in range(len(classes)):
            class_id = classes[g]
            print(class_id)
            classlist.append(class_id)
        cv.imwrite(framename, frame)
        return classlist

def process():
    '''
    print("file loaded")
    returndic = []
    folder = 'videos'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    shutil.copyfile(vidpath, (os.path.join('videos', 'out.mp4')))
    '''

    returndic = []
    for vid in os.listdir('videos'):
        vidmp3 = (vid[:-4])+'.mp3'
        mp3_conversion_command = 'ffmpeg -y -i '+os.path.join('videos', vid)+' -vn -acodec mp3 '+os.path.join('audios',vidmp3)
        os.system(mp3_conversion_command)
        speech_recognition_command = "python -m whisper "+os.path.join('audios',vidmp3)+" --model medium --language en"
        os.system(speech_recognition_command)
        cam = cv2.VideoCapture(os.path.join('videos',vid))
        fps = cam.get(cv2.CAP_PROP_FPS)
        vidtsv=(vid[:-4])+'.tsv'
        with open(vidtsv) as f:
            next(f)
            counter = 0
            for line in f:
                (start, end, text) = line.strip().split("\t")
                sentiment_dict = sid_obj.polarity_scores(text)
                if sentiment_dict['compound'] > 0:
                    tag = "/pos"
                elif sentiment_dict['compound'] < 0:
                    tag = "/neg"
                else:
                    tag = "/neu"
                print(text + "(" + tag + ")")
                framems = (int(end)-int(start))//6
                classlist= []
                for framecount in range(0,6):
                    cam.set(cv2.CAP_PROP_POS_MSEC, int(start)+((framems)*framecount))
                    success, image = cam.read()
                    framename = (str(counter)+ str(framecount) + ".jpg")
                    if detectAndDisplay(image,framename):
                        classlist = classlist + detectAndDisplay(image,framename)
                counter += 1
                classmode = max(set(classlist), key=classlist.count)
                phraseitem = {"tone" : tag, "phrase" : text, "facial" : classmode}
                returndic.append(phraseitem)
    return returndic

class tkinterApp(tk.Tk):


    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, signed_in, program_options, about, history, runwindow):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')
        startbutton = Image.open("getstarted1.png")
        welcomeimg = Image.open("starwelcome1.png")


        wimg = welcomeimg.resize((360, 60))
        loadwimg = ImageTk.PhotoImage(wimg)
        img = startbutton.resize((240, 30))
        loadimage = ImageTk.PhotoImage(img)
        # label of frame Layout 2

        label = tk.Label(self, image = loadwimg, border = '0')
        label.image = loadwimg
        label.place(relx=0.5, rely=0.4, anchor='center')
        # putting the grid in its place by using
        # grid
        #label.grid(row=0, column=4, padx=10, pady=10)



        button1 = tk.Button(self, image = loadimage, bg = 'white', border ='0', cursor = 'hand2',
                             command=lambda: [controller.show_frame(Page1)])
        button1.image = loadimage
        button1.place(relx=0.5, rely=0.5, anchor='center')

        openofflight = Image.open("offbulb.jpg")

        resizeofflight = openofflight.resize((450, 530))

        loadofflight = ImageTk.PhotoImage(resizeofflight)


        lightlabel = tk.Label(self, image=loadofflight, bg='white', border='0')
        lightlabel.image = loadofflight
        lightlabel.place(relx=0.5, rely=0.5, anchor='center')
        lightlabel.lower()

        # putting the button in its place by
        # using grid
        #button1.grid(row=1, column=1, padx=10, pady=10)






# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')
        enterimg = Image.open("enter.png")
        signinimg = Image.open("signin.png")
        eimg = enterimg.resize((270, 50))
        simg = signinimg.resize((250, 50))
        loadenter = ImageTk.PhotoImage(eimg)
        loadsignin = ImageTk.PhotoImage(simg)

        label = tk.Label(self, image=loadenter, bg='white', border='0')
        label.image = loadenter
        label.place(relx=0.5, rely=0.32, anchor='center')

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Skip",
                             command=lambda: controller.show_frame(signed_in))


        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=10, pady=10)
        self.e1 = tk.Entry(self)
        self.e2 = tk.Entry(self, show="*")
        self.e1.place(relx=0.5, rely=0.4, anchor='center')
        self.e2.place(relx=0.5, rely=0.48, anchor='center')



        signbutton = tk.Button(self, image=loadsignin, command=lambda:self.login_clicked(controller), bg='white', border ='0', cursor = 'hand2')
        signbutton.image = loadsignin
        signbutton.place(relx=0.5, rely=0.58, anchor='center')

        createimg = Image.open("create.png")
        cimg = createimg.resize((160, 25))
        loadcreate = ImageTk.PhotoImage(cimg)
        createlabel = tk.Label(self, image = loadcreate, bg = 'white', border = '0')
        createlabel.image = loadcreate
        createlabel.place(relx=0.5, rely=0.65, anchor='center')

    def login_clicked(self, controller):
        username = self.e1.get()
        password = self.e2.get()
        if username == "hacker":
            PlaySound('LBT.wav', SND_FILENAME)
        if username == "admin" and password == "homunculus":
            userid = username
            controller.show_frame(signed_in)

        else:
            messagebox.showerror("Error", "Incorrect username or password")




class signed_in(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')
        openmenu = Image.open("jokemenu1.png")
        openhistory = Image.open("history3.png")
        openrunprog = Image.open("program3.png")
        resizemenu = openmenu.resize((400, 65))
        resizehistory = openhistory.resize((300, 40))
        resizerunprog = openrunprog.resize((300, 40))
        loadmenu = ImageTk.PhotoImage(resizemenu)
        loadhistory = ImageTk.PhotoImage(resizehistory)
        loadrunprog = ImageTk.PhotoImage(resizerunprog)

        openlight = Image.open("bulb.jpg")
        resizelight = openlight.resize((450,530))
        loadlight = ImageTk.PhotoImage(resizelight)
        lightlabel = tk.Label(self, image = loadlight, bg='white', border='0')
        lightlabel.image = loadlight
        lightlabel.place(relx=0.5, rely=0.5, anchor='center')
        lightlabel.lower()

        menulabel = tk.Label(self, image = loadmenu, bg = 'white', border = '0')
        menulabel.image = loadmenu
        menulabel.place(relx=0.5, rely=0.4, anchor='center')

        historybutton = tk.Button(self, image=loadhistory, command = lambda : controller.show_frame(history),bg = 'white', border = '0', cursor = 'hand2')
        historybutton.image = loadhistory
        historybutton.place(relx=0.5, rely=0.65, anchor='center')

        runprogbutton = tk.Button(self,image=loadrunprog, command = lambda : controller.show_frame(program_options), bg = 'white', border = '0', cursor = 'hand2')
        runprogbutton.image = loadrunprog
        runprogbutton.place(relx=0.5, rely=0.75, anchor='center')

        openabout = Image.open("about.png")
        resizeabout = openabout.resize((300, 40))
        loadabout = ImageTk.PhotoImage(resizeabout)
        aboutlabel = tk.Button(self, image=loadabout, command = lambda : controller.show_frame(about), bg='white', border='0', cursor='hand2')
        aboutlabel.image = loadabout
        aboutlabel.image = loadabout
        aboutlabel.place(relx=0.5, rely=0.55, anchor='center')

        opensignout = Image.open("signout.png")
        resizesignout = opensignout.resize((170, 45))
        loadsignout = ImageTk.PhotoImage(resizesignout)
        signoutbutton = tk.Button(self, image=loadsignout, command=lambda: controller.show_frame(StartPage), bg='white',
                                  border='0', cursor='hand2')
        signoutbutton.image = loadsignout
        signoutbutton.place(relx=0.19, rely=0.94, anchor='center')

class program_options(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')
        openoptions = Image.open("options3.png")
        opentags = Image.open("tags.png")
        openfaces = Image.open("faces.png")
        openrun = Image.open("run.png")
        resizeoptions = openoptions.resize((130, 50))
        resizetags = opentags.resize((70, 25))
        resizefaces = openfaces.resize((45, 20))
        resizerun = openrun.resize((120, 40))
        loadoptions = ImageTk.PhotoImage(resizeoptions)
        loadtags = ImageTk.PhotoImage(resizetags)
        loadfaces = ImageTk.PhotoImage(resizefaces)
        loadrun = ImageTk.PhotoImage(resizerun)

        optionslabel = tk.Label(self, image = loadoptions, bg = 'white', border = '0')
        optionslabel.image = loadoptions
        #optionslabel.place(relx=0.5, rely=0.3, anchor='center')

        tick1 = tk.Checkbutton(self, image = loadtags, bg = 'white', border = '0', cursor = 'hand2')
        tick1.image = loadtags
        tick1.place(relx=0.38, rely=0.48, anchor='w')
        tick2 = tk.Checkbutton(self, image = loadfaces, bg = 'white', border = '0', cursor = 'hand2')
        tick2.image = loadfaces
        tick2.place(relx=0.38, rely=0.53, anchor='w')
        openbox = Image.open("rectangle2.png")
        resizebox = openbox.resize((150, 70))
        loadbox = ImageTk.PhotoImage(resizebox)
        boxlabel = tk.Label(self, image = loadbox, bg = 'white', border = '0')
        boxlabel.image = loadbox
        boxlabel.place(relx=0.5, rely=0.51, anchor='center')
        boxlabel.lower()

        opencloud = Image.open("cloud4.png")
        resizecloud = opencloud.resize((500, 450))
        loadcloud = ImageTk.PhotoImage(resizecloud)
        cloudlabel = tk.Label(self, image = loadcloud, bg = 'white', border = '0')
        cloudlabel.image = loadcloud
        cloudlabel.place(relx=0.51, rely=0.37, anchor='center')
        cloudlabel.lower()

        runlabel = tk.Button(self, image = loadrun, command = lambda : controller.show_frame(runwindow), bg = 'white', border = '0', cursor = 'hand2')
        runlabel.image = loadrun
        runlabel.place(relx=0.5, rely=0.64, anchor='center')

        openback = Image.open("back.png")
        resizeback = openback.resize((70, 30))
        loadback = ImageTk.PhotoImage(resizeback)
        backbutton = tk.Button(self, image=loadback, command=lambda: controller.show_frame(signed_in), bg='white',
                               border='0', cursor='hand2')
        backbutton.image = loadback
        backbutton.place(relx=0.5, rely=0.95, anchor='center')



class runwindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')
        dicList = process() #homunculus
        self.processDic(dicList)

    def processDic(self, dicList):
        strcat = ""
        for item in dicList:
            emo = 0
            if item["tone"] == "/neg":
                emo = -float(item["facial"]+1)
            elif item["tone"] == "/pos":
                emo = item["facial"]+1
            else:
                emo = 1.5+float(item["facial"])
            compound = None
            match emo:
                case -1.0:
                    compound = "Anger"
                case 1.0:
                    compound = "Pride"
                case 1.5:
                    compound = "Anger"
                case 2.0:
                    compound = "disgust"
                case 2.5:
                    compound = "disgust"
                case -2.0:
                    compound = "disgust"
                case 3.0:
                    compound = "excitement"
                case 3.5:
                    compound = "Fear"
                case -3.0:
                    compound = "Fear"
                case -4.0:
                    compound = "Sarcasm"
                case 4.0:
                    compound = "Happy"
                case 4.5:
                    compound = "Happy"
                case -5.0:
                    compound = "sad"
                case 5.5:
                    compound = "sad"
                case 5.0:
                    compound = "sad"
                case -6.0:
                    compound = "shocked"
                case 6.0:
                    compound = "surprised"
                case 6.5:
                    compound = "shocked"
                case -7.0:
                    compound = "negative neutral"
                case 7.5:
                    compound = "neutral"
                case 7.0:
                    compound = "positive neutral"
                case _:
                    compound = "no face"
            strcat = strcat+item["phrase"]+" ("+compound+")\n"
      #  print(strcat)
        #print(item["tone"]+','+str(item["facial"])+','+item["phrase"])
        whole = tk.Label(self, text = strcat, fg = 'black', bg = 'white', justify = tk.LEFT, border = '0', wraplength = 500)
        whole.place(relx=0.5, rely=0.1, anchor='center')





class about(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')

        openabout = Image.open("aboutcontent.png")
        resizeabout = openabout.resize((500, 500))
        loadabout = ImageTk.PhotoImage(resizeabout)
        aboutlabel = tk.Label(self, image = loadabout, bg = 'white', border = '0')
        aboutlabel.image = loadabout
        aboutlabel.place(relx=0.5, rely=0.47, anchor='center')

        openback = Image.open("back.png")
        resizeback = openback.resize((70, 30))
        loadback = ImageTk.PhotoImage(resizeback)
        backbutton = tk.Button(self, image = loadback, command = lambda : controller.show_frame(signed_in), bg = 'white', border = '0', cursor = 'hand2')
        backbutton.image = loadback
        backbutton.place(relx=0.5, rely=0.95, anchor='center')

class history(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')

        openhistorypage = Image.open("historypage.png")
        resizehistory = openhistorypage.resize((500, 500))
        loadhistory = ImageTk.PhotoImage(resizehistory)
        historylabel = tk.Label(self, image = loadhistory, bg = 'white', border = '0')
        historylabel.image = loadhistory
        historylabel.place(relx=0.5, rely=0.52, anchor='center')
        openback = Image.open("back.png")
        resizeback = openback.resize((70, 30))
        loadback = ImageTk.PhotoImage(resizeback)
        backbutton = tk.Button(self, image = loadback, command = lambda : controller.show_frame(signed_in), bg = 'white', border = '0', cursor = 'hand2')
        backbutton.image = loadback
        backbutton.place(relx=0.5, rely=0.95, anchor='center')



# Driver Code
app = tkinterApp()
#label_file_explorer = tk.Label(app, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")
app.geometry("500x500")
app.configure(background='white')
icon1 = Image.open("icon.png")
img = ImageTk.PhotoImage(icon1)
app.title("Joke Light")
app.iconbitmap(default="icon.ico")


app.mainloop()