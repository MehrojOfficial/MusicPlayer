"""
</>
Programmer: Mehroj Majidov
Github: https://github.com/MehrojOfficial
Title: "Music Player"
</>
"""

# Imported libraries
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from pygame import mixer # pip install pygame
import time
from mutagen.mp3 import MP3 # pip install mutagen
import pygame
from PIL import ImageTk, Image
import music_tag # pip install music_tag

# UI
root = Tk()
root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0')
root.title('JARVIS Music Player')
root.state('zoomed')
root.configure(bg = '#0f0f0f')
root.iconbitmap(r"data/icon.ico")

f1 = Frame(root, bd=0, bg="black", relief=SUNKEN)
f2 = Frame(root, bd=0, bg="#0f0f0f", relief=SUNKEN)

f1.place(relx=0, relheight=1, relwidth=1)
f2.place(rely=0.8, relheight=1, relwidth=1)

# Variables
playlist = []
music_title = ''
status = 'notstarted'
initialize = False
queue_number = 0
values = 0
muter = 'unmute'
def_muter = 0

# Main-control-button images
music_img = Image.open('data/music-icon.png')
music_img = music_img.resize((50,50), Image.ANTIALIAS)
music_img = ImageTk.PhotoImage(music_img)

previous_img = Image.open('data/previous-icon.png')
previous_img = previous_img.resize((25,25), Image.ANTIALIAS)
previous_img = ImageTk.PhotoImage(previous_img)

next_img = Image.open('data/next-icon.png')
next_img = next_img.resize((25,25), Image.ANTIALIAS)
next_img = ImageTk.PhotoImage(next_img)

pause_img = Image.open('data/pause-icon.png')
pause_img = pause_img.resize((80,80), Image.ANTIALIAS)
pause_img = ImageTk.PhotoImage(pause_img)

play_img = Image.open('data/play-icon.png')
play_img = play_img.resize((80,80), Image.ANTIALIAS)
play_img = ImageTk.PhotoImage(play_img)

volume_high = Image.open('data/volume-high.png')
volume_high = volume_high.resize((30,23), Image.ANTIALIAS)
volume_high_img = ImageTk.PhotoImage(volume_high)

volume_mute = Image.open('data/volume_mute.png')
volume_mute = volume_mute.resize((30,20), Image.ANTIALIAS)
volume_mute_img = ImageTk.PhotoImage(volume_mute)

load_btn = Image.open('data/load.png')
load_btn = load_btn.resize((40,40), Image.ANTIALIAS)
load_btn_img = ImageTk.PhotoImage(load_btn)

music_name = None
music_artist = None


# Background images
count = -1

jarvis_images = ["data/jarvis.png",
  "data/jarvis2.png",
  "data/jarvis3.png",
  "data/jarvis4.png",
  "data/jarvis5.png",
  "data/jarvis6.png",
  "data/jarvis7.png",
  "data/jarvis8.png",
  "data/jarvis9.png",
  "data/jarvis10.png",
  "data/jarvis11.png"
]

# Default background
jarvis_pic = Image.open(jarvis_images[5]).resize((900,500), Image.ANTIALIAS)
jarvis_pic2 = ImageTk.PhotoImage(jarvis_pic)
label = Label(root, image = jarvis_pic2,borderwidth=0)
label.place(x=240,y=10)

# Updating animation
def img_update():
    global count,status
    if status == 'playing':
        if count == 10:
            jarvis_img = Image.open(jarvis_images[count])
            jarvis_img = jarvis_img.resize((900,500), Image.ANTIALIAS)
            count = 0
        else:
            count += 1
            jarvis_img = Image.open(jarvis_images[count])
            jarvis_img = jarvis_img.resize((900,500), Image.ANTIALIAS)
        
        jarvis_img2 = ImageTk.PhotoImage(jarvis_img)
        label.configure(image = jarvis_img2)
        label.image = jarvis_img2 
    root.after(1,img_update)

# Getting object or length of music in pieces
def convert(audio):
    try:
        seconds = int(audio)
    except:
        seconds = int(audio.get_length())
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return hours, mins, seconds

# Zeroic numbers
def zero_add(number):
  if len(str(number)) == 1:
    number = f'0{number}'
  else:
    pass
  return number

# Slider Styles
def set_img_color(img, color):
    """Change color of PhotoImage img."""
    pixel_line = "{" + " ".join(color for i in range(img.width())) + "}"
    pixels = " ".join(pixel_line for i in range(img.height()))
    img.put(pixels)

slider_width = 15
slider_height = 10
img_slider = PhotoImage('img_slider', width=slider_width, height=slider_height, master=root)
set_img_color(img_slider, "#FFFFFF")
img_slider_active = PhotoImage('img_slider_active', width=slider_width, height=slider_height, master=root)
set_img_color(img_slider_active, '#606A75')
style = ttk.Style(root)
style.theme_use('winnative')
style.element_create('custom.Horizontal.Scale.slider', 'image', img_slider,
                     ('active', img_slider_active))
style.layout('custom.Horizontal.TScale',
             [('Horizontal.Scale.trough',
               {'sticky': 'nswe',
                'children': [('custom.Horizontal.Scale.slider',
                              {'side': 'left', 'sticky': ''})]})])
style.configure('custom.Horizontal.TScale', background='black', foreground='grey',
                troughcolor='#535353')

class MusicMake:
    def __init__(self,music_location):
        tag = music_tag.load_file(music_location)
        m3 = MP3(music_location)
        self.title = tag['title']
        self.artist = tag['artist']
        self.length = m3.info.length
        self.location = music_location

    def get_title(self):
        return self.title
    def get_artist(self):
        return self.artist
    def get_length(self):
        return self.length

# Loading music and making playlist
def load():
    global playlist
    global initialize
    global status
    files = filedialog.askopenfilenames(title = 'Select an Mp3 files only', filetypes=(('MP3 files', '*.mp3'),('All files', '*.mp3')))
    
    playlist = []
    if initialize:
        initialize = False
    status = 'notstarted'

    if files:
        for file in files:
            music = MusicMake(file)
            playlist.append(music)

    title_update(playlist[queue_number])
    artist_update(playlist[queue_number])
    full_time_display()

    print(playlist)

# Updating music title
def title_update(music_object):
    global music_title
    title = music_object.get_title()
    name = music_object.get_title()
    if title:
        music_title.configure(text = title)
    else:
        music_title.configure(text = "JARVIS")

# Updating music artist
def artist_update(music_object):
    global music_artists
    artist = music_object.get_artist()
    if artist:
        music_artists.configure(text = artist)
    else:
        music_artists.configure(text = "MUSIC PLAYER")

# Next Music
def music_change_up():
    global queue_number
    if playlist[queue_number] != playlist[-1]:
        queue_number += 1
        music_file = playlist[queue_number]
        f = music_tag.load_file(music_file.location)
        name = music_file.get_title()
        artist = music_file.get_artist()

        title_update(music_file)
        artist_update(music_file)
        full_time_display()
        length = music_file.get_length()
        slider.configure(to = length)

# Previous Music
def music_change_down():
    global queue_number
    if queue_number > 0:
        queue_number -= 1
        music_file = playlist[queue_number]
        f = music_tag.load_file(music_file.location)
        name = music_file.get_title()
        artist = music_file.get_artist()
        
        title_update(music_file)
        artist_update(music_file)
        full_time_display()
        length = music_file.get_length()
        slider.configure(to = length)

# Starting to play
def play():
    global status
    global initialize
    global slider
    global values
    if len(playlist) != 0 and status == 'notstarted':
        if not initialize:
            mixer.init()
        mixer.music.load(playlist[queue_number].location)
        mixer.music.play()
        status = 'playing'
        Play.configure(image=pause_img)
    
    elif len(playlist) != 0 and status == 'unconditional_slide':
        mixer.music.play(start = values)
        status = 'playing'
        Play.configure(image=pause_img)

    else:
        if status == 'playing':
            mixer.music.pause()
            status = 'paused'
            Play.configure(image = play_img)

        else:
            if status == 'paused':
                mixer.music.unpause()
                status = 'playing'
                Play.configure(image=pause_img)

            if status == 'the-end':
                current_time.configure(text='00:00')
                slider.configure(value = 0)
                status = 'notstarted'
                values = 0
                music_change_up()
                play()
    length = playlist[queue_number].get_length()
    slider.configure(to = length)

    full_time_display()

# Starts infinite loop of slider
def start_slider():
    slide()

# Displays full music length
def full_time_display():
    hours, mins, seconds = convert(playlist[queue_number])
    mins = zero_add(mins)
    seconds = zero_add(seconds)

    if hours == 0:
        full_times = f'{mins}:{seconds}'
    else:
        hours = zero_add(hours)
        full_times = f'{hours}:{mins}:{seconds}'
    full_time.config(text=full_times)

# Displays currently played music time
def current_time_display():
    seconds = slider.get()
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    mins = zero_add(mins)
    seconds = zero_add(seconds)
    if hours == 0:
        current_times = f'{mins}:{seconds}'
    else:
        hours = zero_add(hours)
        current_times = f'{hours}:{mins}:{seconds}'
    current_time.config(text = current_times)

# Music Progressbar updater
def slide():
    global status
    global values

    if status == 'paused' or status == 'the-end' or status == "notstarted":
        root.after(1000,slide)
        return
    else:
        slider.configure(value = values)
        current_time_display()
        values += 1

    if full_time['text'] != current_time['text']:
        root.after(1000,slide)
    else:
        if playlist[-1] == playlist[queue_number]:
            play()
            status = 'the-end'
        else:
            next_m()
            root.after(1000,slide)

# Manual slider editor
def update_slide(event=None):
    global values, status
    if status == 'playing':
        a = slider.get()
        a = round(a)
        mixer.music.play(start = a)
        slider.configure(value = a)
        values = a
    else:
        status = 'unconditional_slide'
        a = slider.get()
        a = round(a)
        slider.configure(value = a)
        values = a

# Volume changer
def update_volume(event=None):
    global initialize, muter, off_muter
    a = slider_volume.get()
    a = round(a)
    volume_info.configure(text = f'{a}')
    if initialize:
        pygame.mixer.music.set_volume(int(a)/100)
    else:
        mixer.init()
        initialize = True
        pygame.mixer.music.set_volume(int(a)/100)
    if a == 0:
        Volume.configure(image=volume_mute_img)
    else:
        Volume.configure(image=volume_high_img)

# Next music button
def next_m():
    global status, values, playing_state
    if playlist[queue_number] != playlist[-1]:
        slider.configure(value = 0)
        status = 'notstarted'
        values = 0
        music_change_up()
        play()

# Previous music button
def previous_m():
    global status, values, playing_state
    if playlist[queue_number] != playlist[0]:
        mixer.music.pause()
        slider.configure(value = 0)
        status = 'notstarted'
        values = 0
        music_change_down()
        play()

# Mute/Unmute button
def mute_unmute():
    global muter, def_muter, off_muter
    if not initialize:
        mixer.init()
    if muter == 'unmute':
        def_muter = round(slider_volume.get())
        volume_info.configure(text = '0')
        pygame.mixer.music.set_volume(0)
        slider_volume['value'] = 0
        muter = 'mute'
        Volume.configure(image=volume_mute_img)
    else:
        volume_info.configure(text = f'{def_muter}')
        pygame.mixer.music.set_volume(def_muter)
        slider_volume['value'] = def_muter
        muter = 'unmute'
        Volume.configure(image=volume_high_img)

# UI elemets

current_time = Label(root,text='00:00',background='#0f0f0f', foreground='#FFFFFF',font = 'Helvetica 10 bold')
current_time.place(x=410,y=692)

full_time = Label(root,text='00:00',background='#0f0f0f', foreground='#FFFFFF',font = 'Helvetica 10 bold')
full_time.place(x=970,y=692)

volume_info = Label(root,text='100',background='#0f0f0f',foreground='#FFFFFF',font = 'Helvetica 12 bold')
volume_info.place(x=1300,y=660)

slider = ttk.Scale(root, from_=0, to=1, value=0, length=500, orient=HORIZONTAL, command=update_slide, style='custom.Horizontal.TScale')
slider.place(x=460,y=698)

slider_volume = ttk.Scale(root, from_=0, to=100, value=100, length=100, orient=HORIZONTAL, command=update_volume, style='custom.Horizontal.TScale')
slider_volume.place(x=1190,y=667)

music_label = Label(root, image = music_img,bg = '#0f0f0f')
music_label.place(x=20,y=650)

music_title = Label(root, text = 'Jarvis', bg = '#0f0f0f', width = 25, anchor = 'w', justify = RIGHT, fg = '#FFFFFF', font = 'Helvetica 15 bold')
music_title.place(x=90,y=650)

music_artists = Label(root, text = 'Music Player',  bg = '#0f0f0f',fg = '#FFFFFF', font = 'Helvetica 10 bold')
music_artists.place(x=90,y=680)

Load = Button(root, image=load_btn_img,  width = 50, bg = '#0f0f0f', highlightthickness = 0, bd = 0, activebackground='#0f0f0f', command = load)
Play = Button(root, image = play_img, highlightthickness = 0, bd = 0, bg = '#0f0f0f', activebackground='#0f0f0f', command = play)
Next = Button(root, image = next_img, highlightthickness = 0, bd = 0, bg = '#0f0f0f', activebackground='#0f0f0f', command = next_m)
Previous = Button(root, image = previous_img, highlightthickness = 0, bd = 0, bg = '#0f0f0f', activebackground='#0f0f0f', command = previous_m)
Volume = Button(root, image=volume_high_img, bg = '#0f0f0f', highlightthickness = 0, bd = 0, activebackground='#0f0f0f', command = mute_unmute)

Load.place(x=0,y=20)
Play.place(x=660,y=610)
Next.place(x=774,y=639)
Previous.place(x=600,y=639)
Volume.place(x=1150,y=660)

# Animations
def enter(event=None):
    music_title.configure(bg='#292727')
def leave(event=None):
    music_title.configure(bg = '#0f0f0f')
music_title.bind('<Enter>', enter)
music_title.bind('<Leave>', leave)

def enter(event=None):
    Load.configure(bg='#292727')
def leave(event=None):
    Load.configure(bg = '#0f0f0f')
Load.bind('<Enter>', enter)
Load.bind('<Leave>', leave)

def enter(event=None):
    music_artists.configure(bg='#292727')
def leave(event=None):
    music_artists.configure(bg = '#0f0f0f')
music_artists.bind('<Enter>', enter)
music_artists.bind('<Leave>', leave)

start_slider()
img_update()

root.mainloop()