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


model = YOLO("best.pt")
global userid
global filename

# Load Haar Classifier for face detection
face_cascade_name = ".\\face.xml"  # args.face_cascade
eyes_cascade_name = ".\\eyes.xml"  # args.eyes_cascade
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


def detect_and_display(screen):
    """
    Input:
    -screen: a frame from the video
    Output:
    -classlist: a list of rectangles encompassing faces
    """
    classlist = []

    #Prep images and use Haar Classifier for face detection
    screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY) # Convert to grayscale
    screen_gray = cv.equalizeHist(screen_gray)
    faces = face_cascade.detectMultiScale(screen_gray)

    if any(map(len, faces)):
        # Picks the largest face in the picture by sorting the face list
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        frame = screen.copy()

        #Cuts a square frame around the face
        dim = min(w,h)
        frame = frame[y:y + dim, x:x + dim]

        #Resize face to prep for CNN
        if dim != 48:
            if dim < 48:
                frame = cv.resize(frame, (48, 48), interpolation=cv.INTER_LINEAR)
            else:
                frame = cv.resize(frame, (48, 48), interpolation=cv.INTER_AREA)
        frame = cv.resize(frame, (48, 48), interpolation=cv.INTER_LINEAR)

        #Run CNN model and gather results
        results = model(frame)
        r = results[0]
        classes = r.boxes.cls.tolist()

        #Collect classes into list
        for g in range(len(classes)):
            class_id = classes[g]
            classlist.append(class_id)
        return classlist


def process():
    """
    Input: none (reads files)
    Output:
    -returndic: a dictionary of phrases with tone tags and facial emotions
    """
    returndic = []

    #Process videos
    for vid in os.listdir('videos'):

        # Extract mp3 files from mp4 videos
        vidmp3 = (vid[:-4])+'.mp3'
        mp3_conversion_command = 'ffmpeg -y -i '+os.path.join('videos', vid)+' -vn -acodec mp3 '+os.path.join('audios',vidmp3)
        os.system(mp3_conversion_command)

        # Extract speech from mp3 file
        speech_recognition_command = "python.exe -m whisper "+os.path.join('audios',vidmp3)+" --model medium --language en"
        os.system(speech_recognition_command)

        # Load video into OpenCV
        cam = cv2.VideoCapture(os.path.join('videos',vid))
        vidtsv=(vid[:-4])+'.tsv'
        with open(vidtsv) as f:
            next(f)
            counter = 0
            for line in f:
                (start, end, text) = line.strip().split("\t") # Grab timestamps for each line in the video
                sentiment_dict = sid_obj.polarity_scores(text) # Produce text sentiments from sentiment analysis
                if sentiment_dict['compound'] > 0:
                    tag = "/pos"
                elif sentiment_dict['compound'] < 0:
                    tag = "/neg"
                else:
                    tag = "/neu"
                framems = (int(end)-int(start))//6
                classlist= []
                for framecount in range(0,6): # Analyses 6 frames per phrase
                    cam.set(cv2.CAP_PROP_POS_MSEC, int(start)+(framems*framecount))
                    success, image = cam.read()
                    if detect_and_display(image):
                        classlist = classlist + detect_and_display(image)
                counter += 1
                classmode = max(set(classlist), key=classlist.count) # Select emotion which occurs most
                # Compile each line into phrase, text sentiment, and face emotion
                phraseitem = {"tone" : tag, "phrase" : text, "facial" : classmode}
                returndic.append(phraseitem)
    return returndic

# Removes excess subtitle files from calling whisper
for item in os.listdir("."):
    if item.endswith(".srt") or item.endswith(".txt") or item.endswith(".json") or item.endswith(".tsv") or item.endswith(".vtt"):
        os.remove(item)

class TkInterApp(tk.Tk):


    # __init__ function for class TkInterApp
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
        for F in (StartPage, Page1, SignedIn, ProgramOptions, About, History, RunWindow):
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
                             command=lambda: controller.show_frame(SignedIn))


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
            controller.show_frame(SignedIn)

        else:
            messagebox.showerror("Error", "Incorrect username or password")




class SignedIn(tk.Frame):
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

        historybutton = tk.Button(self, image=loadhistory, command = lambda : controller.show_frame(History), bg ='white', border ='0', cursor ='hand2')
        historybutton.image = loadhistory
        historybutton.place(relx=0.5, rely=0.65, anchor='center')

        runprogbutton = tk.Button(self, image=loadrunprog, command = lambda : controller.show_frame(ProgramOptions), bg ='white', border ='0', cursor ='hand2')
        runprogbutton.image = loadrunprog
        runprogbutton.place(relx=0.5, rely=0.75, anchor='center')

        openabout = Image.open("about.png")
        resizeabout = openabout.resize((300, 40))
        loadabout = ImageTk.PhotoImage(resizeabout)
        aboutlabel = tk.Button(self, image=loadabout, command = lambda : controller.show_frame(About), bg='white', border='0', cursor='hand2')
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

class ProgramOptions(tk.Frame):
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

        runlabel = tk.Button(self, image = loadrun, command = lambda : controller.show_frame(RunWindow), bg ='white', border ='0', cursor ='hand2')
        runlabel.image = loadrun
        runlabel.place(relx=0.5, rely=0.64, anchor='center')

        openback = Image.open("back.png")
        resizeback = openback.resize((70, 30))
        loadback = ImageTk.PhotoImage(resizeback)
        backbutton = tk.Button(self, image=loadback, command=lambda: controller.show_frame(SignedIn), bg='white',
                               border='0', cursor='hand2')
        backbutton.image = loadback
        backbutton.place(relx=0.5, rely=0.95, anchor='center')



class RunWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white')
        dicList = process() #homunculus
        self.processDic(dicList)

    def processDic(self, dic_list):
        strcat = ""
        for token in dic_list:
            if token["tone"] == "/neg":
                emo = -float(token["facial"]+1)
            elif token["tone"] == "/pos":
                emo = token["facial"]+1
            else:
                emo = 1.5+float(token["facial"])
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
            strcat = strcat+token["phrase"]+" ("+compound+")\n"
        whole = tk.Label(self, text = strcat, fg = 'black', bg = 'white', justify = tk.LEFT, border = '0', wraplength = 500)
        whole.place(relx=0.5, rely=0.1, anchor='center')





class About(tk.Frame):
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
        backbutton = tk.Button(self, image = loadback, command = lambda : controller.show_frame(SignedIn), bg ='white', border ='0', cursor ='hand2')
        backbutton.image = loadback
        backbutton.place(relx=0.5, rely=0.95, anchor='center')

class History(tk.Frame):
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
        backbutton = tk.Button(self, image = loadback, command = lambda : controller.show_frame(SignedIn), bg ='white', border ='0', cursor ='hand2')
        backbutton.image = loadback
        backbutton.place(relx=0.5, rely=0.95, anchor='center')



# Driver Code
app = TkInterApp()
#label_file_explorer = tk.Label(app, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")
app.geometry("500x500")
app.configure(background='white')
icon1 = Image.open("icon.png")
#img = ImageTk.PhotoImage(icon1)
app.title("Joke Light")
app.iconbitmap(default="icon.ico")


app.mainloop()