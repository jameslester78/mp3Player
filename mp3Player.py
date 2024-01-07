
import tkinter as tk
import tinytag

from tkinter import filedialog
from pygame import mixer

def addSongs():

    #add songs to the current tracklist
   
    #open up a dialog box to allow the user to find a folder of mp3 files
    files=filedialog.askopenfilenames(filetypes=(("mp3 Files","*.mp3"),))

    #user can select multiple files, lets process them
    for _ in files:
        #use tiny tag to pull out the attributes from the files
        songInfo = tinytag.TinyTag.get(_)
        #we want the artist and song title
        label = f'{songInfo.artist} - {songInfo.title}'
        #lets add this to the GUI
        queueList.insert(tk.END,label)
        #and lets add GUI text to a dictionary where we also store the file path
        songDict[label] = _

def play(event = None): #an event may be passed to the function depending on how it is called, we
                        #dont do anything with this, but the functiion needs to accept it for tkinter
                        #to do its stuff - specifically with the double click command 

    #play the currently selected song

    #get the highlighted song
    song=queueList.get(tk.ACTIVE)

    if song != '':    

        #get the file location from the dictionary
        songLoc = songDict[song]

        #load the song and play it
        mixer.music.load(songLoc)
        mixer.music.play()

    else:

        print('no track selected') 




def playall (event = None):

    #play all songs on track list

    #get all items from the list
    allsongs = queueList.get(0,tk.END)

    if (len(allsongs)) != 0:

        #lets enumerate and for each song
        for _ in enumerate(allsongs):

            #if its the first one, load it and play
            if _[0] == 0:
                songLoc = songDict[_[1]]
                mixer.music.load(songLoc)
            #for everything else queue it up
            else:
                songLoc = songDict[_[1]]
                mixer.music.queue(songLoc)
        #and finally press play                
        mixer.music.play()        

    else: 
        print('Nothing selected')



def stop(event = None):
    #stop the music from playing
    mixer.music.stop()    


def save(event = None):

    #save the current playlist

    #get all the songs from the list
    allsongs = queueList.get(0,tk.END)
    #print (allsongs)

    playlist = ''

    #add each song to playlist string
    for _ in allsongs:
        #print (songDict[_])
        playlist += songDict[_] + '\n'
    
    #remove the final new line char
    playlist = playlist[0:-1]
    #print (playlist)

    #ask the user where they want to save the m3u file
    files=filedialog.asksaveasfilename(defaultextension="*.m3u",filetypes=(('M3U Playlist','*.m3u'),))
    #print (files)

    #write the file
    with open(files, 'w') as file:
        file.write (playlist)


def load(event = None):

    #ask user to locate the playlist
    file = filedialog.askopenfile(filetypes=(('M3U Playlist','*.m3u'),))

    #print (file.name)

    #read each line of the file
    with open(file.name, 'r') as file:
        lines = file.readlines()

    songs = []

    #add each line of the playlist to a list, removing any newlines
    for _ in lines:
        
        if _.endswith('\n'):
            songs.append(_[0:-1])
        else:
            songs.append(_)

    #print (songs)
    
    #clear the current track list
    queueList.delete(0,tk.END)


    #using tinyTag populate the tracklist with song names and artist names, and populate the song dictionary that maps
    #these bit of info to the file location

    for _ in songs:
        songInfo = tinytag.TinyTag.get(_)
        label = f'{songInfo.artist} - {songInfo.title}'
        queueList.insert(tk.END,label)
        songDict[label] = _
    
    #print (songDict)


def clear(event = None):
    #clear the track list
    queueList.delete(0,tk.END)

#initialise the mp3 player
mixer.init()

#configure the GUI

window = tk.Tk()
window.title ('mp3 player')
window.geometry("600x200")

listLabel = tk.Label(window,text="Track List:")
queueList = tk.Listbox(window,width=50)

addToQueue = tk.Button(window,text="Add Songs",command=addSongs,width=15)
clearButton = tk.Button(window,text="Clear",command=clear,width=15)
scroll = tk.Scrollbar(window ,orient="vertical", command=queueList.yview)

#The scroll bar should operate the list box
queueList.configure(yscrollcommand=scroll.set)
#If we double click the listbox we want to play the selected song
queueList.bind("<Double-Button-1>", play)

stopButton = tk.Button(window,text="Stop",command=stop,width=15)
#play button can be either single track or All, we track the selected operation here
play_type = tk.StringVar(window) 
playMenu = tk.OptionMenu(window, play_type, *['Play','Play All']) 
playMenu.config(width=12)
#set the default
play_type.set("Play All") 


def doIt(*args):
    #function gets called when the play button is pushed
    #call either the play or play all function

    #print (play_type.get())
    if play_type.get() == 'Play':
        play()
    if play_type.get() == 'Play All':
        playall()        

#when the play type variable is set, call the doIt function
play_type.trace("w", doIt)

listLabel.place(x=10,y=0)
queueList.place(x=10,y=20)
addToQueue.place(x=330,y=20)
clearButton.place(x=450,y=20)
playMenu.place(x=329,y=60)
stopButton.place(x=450,y=60, height=29)
scroll.place(x=305,y=20, height=170)

#add the playlist file save/load to a menu bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Load", command=load)
menubar.add_cascade(label='Playlist',menu=filemenu)

#add the menu to the GUI
window.config(menu=menubar)

songDict ={}

#open the form
window.mainloop()