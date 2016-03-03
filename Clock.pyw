#!/usr/bin/env python
# -*- coding: cp1250 -*-

from tkinter import *
from time import localtime, strftime
from winsound import Beep
import sqlite3 as lite
from tkinter import font as tkFont
from tkinter import colorchooser
from tkinter import filedialog
import os

import win32gui
import win32con

try:
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Options')
        options = cur.fetchall()[0]

    (
    alarm, color1, color2, color3, position, font, beep, move, ontop, size, format, file, player, favourites) = options[
                                                                                                                1:]
except:
    (alarm, color1, color2, color3, position, font, beep, move, ontop, size, format, file, player, favourites) = (
    '10:45', 'white', 'black', 'red', '+10+10', 'arial', 0, 0, 0, 50, '%H:%M:%S', '', '', "[]")
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE Options(Id INTEGER PRIMARY KEY,
                       alarm TEXT,
                       color1 TEXT,
                       color2 TEXT,
                       color3 TEXT,
                       position TEXT,
                       font TEXT,
                       beep INT,
                       move INT,
                       ontop INT,
                       size INT,
                       format TEXT,
                       file TEXT,
                       player TEXT,
                       favourites TEXT)''')
        cur.execute(
            '''INSERT INTO Options(alarm,color1,color2,color3,position,font,beep,move,ontop,size,format,file,player,favourites)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (alarm, color1, color2, color3, position, font, beep, move, ontop, size, format, file, player,
             str(favourites)))

root = Tk()
root.title('Ura1234')
root.geometry(position)
root.attributes('-alpha', 0.8)
root.attributes('-topmost', 1)
root.overrideredirect(True)

######################################################################
hwnds = []
self = 0
screen_size = (0, 0, root.winfo_screenwidth(), root.winfo_screenheight())
hwnd1 = 0
flag = 0


def on_top():
    global flag
    root.attributes('-topmost', 1)
    root.attributes('-topmost', 0)
    flag = 1


def bottom():
    # win32con.SWP_SHOWWINDOW|win32con.SWP_NOMOVE | win32con.SWP_NOSIZE = 67
    # win32con.HWND_BOTTOM = 1
    global self
    win32gui.SetWindowPos(self, 1, 0, 0, 0, 0, 67)


def enumHandler(hwnd, lParam):
    global hwnds
    if win32gui.IsWindowVisible(hwnd):
        hwnds.append(hwnd)


def gen_name(*args):
    global hwnds, hwnd1, flag
    hwnds = []
    win32gui.EnumWindows(enumHandler, None)

    for i in range(2, hwnds.index(self)):
        try:
            if win32gui.GetWindowRect(hwnds[i]) == screen_size and win32gui.GetWindowText(hwnds[i]) == '':
                hwnd1 = hwnds[2]
                on_top()
        except:
            # okno obstaja, ko uporabiš EnumWindows, a je že uniceno, ko kliceš GetWindowRect
            continue

    if flag and hwnd1 not in hwnds:
        bottom()
        flag = 0

    root.after(150, gen_name)


def enumHandler2(hwnd, lParam):
    global self, hwnd1
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) == 'Ura1234':
            self = hwnd
            hwnd1 = hwnd


def get_self(*args):
    win32gui.EnumWindows(enumHandler2, None)


def dummy_name():
    root.after(500, get_self)
    root.after(1000, gen_name)

##    root.after(1500, bottom)


dummy_name()
######################################################################







win, win2, win3 = None, None, None

curr_time = StringVar()
curr_time.set(strftime(format, localtime()))
hours = StringVar()
hours.set(alarm[:2])
minutes = StringVar()
minutes.set(alarm[-2:])
format1 = StringVar()
format1.set(format)
move1 = IntVar()
move1.set(move)
ontop1 = IntVar()
ontop1.set(ontop)
x1 = IntVar()
x1.set(int(position.split('+')[1]))
y1 = IntVar()
y1.set(int(position.split('+')[2]))
alarm_active = False
favourites = eval(favourites)
e3_var = StringVar()
e3_var.set(file)
e4_var = StringVar()
e4_var.set(player)

a = Label(root, textvariable=curr_time, font=(font, -size, 'bold'), anchor=CENTER, bg=color2, fg=color1)
a.grid(row=0, column=0)

win_x, win_y = None, None


def StartMove(event):
    global win_x, win_y
    win_x = event.x
    win_y = event.y


def StopMove(event):
    global win_x, win_y
    win_x, win_y = None, None


def OnMotion(event):
    global win_x, win_y, position
    deltax = event.x - win_x
    deltay = event.y - win_y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    x1.set(x)
    y1.set(y)
    position = '+%s+%s' % (x, y)
    root.geometry(position)


def save_options():
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()

        cur.execute('DELETE FROM Options WHERE Id = 1')
        cur.execute(
            '''INSERT INTO Options(alarm,color1,color2,color3,position,font,beep,move,ontop,size,format,file,player,favourites)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (alarm, color1, color2, color3, position, font, beep, move, ontop, size, format, file, player,
             str(favourites)))


def color():
    global alarm_active
    if alarm_active:
        a.config(fg=color3)
    else:
        a.config(fg=color1)


def check(what, max):
    try:
        if int(what) < max and int(what) >= 0:
            return what
        else:
            return False
    except ValueError:
        return False


def correct(sth):
    if len(sth) == 1:
        return '0' + sth
    else:
        return sth


def alarm_set(*args):
    global alarm_active, alarm, win
    if alarm_active:
        alarm_active = False
        color()
        try:
            win.destroy()
            win = None
        except:
            pass
    else:
        h = correct(hours.get())
        m = correct(minutes.get())
        if check(h, 24) and check(m, 60):
            alarm = h + ':' + m
            alarm_active = True
            color()
            try:
                win.destroy()
                win = None
            except:
                pass
    if args:
        StartMove(args[0])


def alarm_window(x):
    global win, button
    if win: return 0  # prevent more than one alarm window
    win = Toplevel(root)
    win.iconbitmap('Ura.ico')
    x = position.split('+')
    win.geometry('+' + str(int(x[1]) + 15) + '+' + str(int(x[2]) + 50))
    win.title('Alarm')
    win.focus_set()

    def _delete_window():
        global win
        try:
            win.destroy()
            win = None
        except:
            pass

    Label(win, text='Nastavi alarm:', anchor=W, justify=LEFT).grid(row=0, column=0, columnspan=10)

    hours_entry = Entry(win, textvariable=hours, width=4)
    minutes_entry = Entry(win, textvariable=minutes, width=4)

    Label(win, text=' ').grid(row=1, column=0)
    hours_entry.grid(row=1, column=1)
    Label(win, text=':').grid(row=1, column=2)
    minutes_entry.grid(row=1, column=3)
    Label(win, text=' ').grid(row=1, column=4)

    Button(win, text='Alarm' if not alarm_active else 'Izklopi', command=alarm_set).grid(row=1, column=5)

    win.bind_all('<Return>', alarm_set)
    win.protocol('WM_DELETE_WINDOW', _delete_window)


def uporabi(*args):
    global size, position, file, player
    size = int(v.get())
    position = '+' + str(x1.get()) + '+' + str(y1.get())
    root.geometry(position)
    a.config(font=(font, -size, 'bold'))
    file = e3_var.get()
    player = e4_var.get()
    save_options()
    return 0


def v_redu():
    global win2
    uporabi()
    save_options()
    win2.destroy()
    win2 = None


def save_close(*args):
    save_options()
    root.destroy()


def get_color(which):
    global color1, color2, color3, l1, l2, l3
    new = colorchooser.askcolor()[1]
    if new:
        if which == 2:
            color2 = new
            a.config(bg=color2)
            l2.config(bg=color2)
            pass
        elif which == 1:
            color1 = new
            l1.config(bg=color1)
            pass
        else:
            color3 = new
            l3.config(bg=color3)
            pass
        color()


def choose_font():
    global aux_font
    master = Toplevel(root)

    text_frame = Frame(master, height=100, width=300)
    text_frame.grid(row=0, column=3, rowspan=2)
    text_frame.grid_propagate(False)
    text_item = Label(text_frame, text='9876543210:', font=(font, -60, 'bold'))
    text_item.grid(row=0, column=0)

    frame1 = Frame(master)
    frame1.grid(row=0, column=0, rowspan=2)
    list1 = Listbox(frame1, bd=2)
    scrollbar = Scrollbar(frame1, orient=VERTICAL)
    scrollbar.config(command=list1.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    list1.configure(yscrollcommand=scrollbar.set)

    for f in sorted(tkFont.families()):
        list1.insert(END, f)
    list1.pack()

    frame2 = Frame(master)
    frame2.grid(row=0, column=2, rowspan=2)
    list2 = Listbox(frame2, bd=2)
    scrollbar2 = Scrollbar(frame2, orient=VERTICAL)
    scrollbar2.config(command=list2.yview)
    scrollbar2.pack(side=RIGHT, fill=Y)
    list2.configure(yscrollcommand=scrollbar.set)
    for f in favourites:
        list2.insert(END, f)
    list2.pack()

    def add_to_favourites():
        global favourites
        sel = list1.curselection()
        if len(sel) > 0:
            font_name = list1.get(sel[0])
            list2.insert(END, font_name)
            favourites.append(font_name)

    def remove_from_favourites():
        global favourites
        sel = list2.curselection()
        if len(sel) > 0:
            font_name = list2.get(sel[0])
            list2.delete(sel[0])
            favourites.remove(font_name)

    Button(master, text='Dodaj', command=add_to_favourites).grid(row=0, column=1)
    Button(master, text='Odstrani', command=remove_from_favourites).grid(row=1, column=1)

    def font_changed(ev=None, x=1):
        global aux_font
        list_cur = [list1, list2][x]
        sel = list_cur.curselection()
        font_name = list_cur.get(sel[0]) if len(sel) > 0 else "Times"
        text_item.config(font=(font_name, -60, 'bold'))
        aux_font = font_name

    list1.bind("<<ListboxSelect>>", lambda arg: font_changed(arg, x=0))
    list2.bind("<<ListboxSelect>>", lambda arg: font_changed(arg, x=1))

    def uporabi_font(*args):
        global font, a, size, aux_font
        font = aux_font
        a.config(font=(font, -size, 'bold'))

    Button(master, text='Izhod', command=lambda: master.destroy()).grid(row=20, column=3)
    Button(master, text='Uporabi', command=uporabi_font).grid(row=20, column=4)

    master.bind_all('<Return>', uporabi_font)


def move_fnc():
    global move
    move = move1.get()
    if move:
        root.bind("<ButtonPress-1>", StartMove)
        root.bind("<ButtonRelease-1>", StopMove)
        root.bind("<B1-Motion>", OnMotion)
    else:
        try:
            root.unbind("<ButtonPress-1>")
            root.unbind("<ButtonRelease-1>")
            root.unbind("<B1-Motion>")
        except:
            pass


move_fnc()


def ontop_fnc():
    global ontop
    ontop = ontop1.get()
    if ontop:
        root.wm_attributes("-topmost", 1)
    else:
        root.wm_attributes("-topmost", 0)


ontop_fnc()


def options_window(x):
    global win2, button, l1, l2, l3, v, beep
    if win2: return 0  # prevent more than one options window
    win2 = Toplevel(root)
    win2.iconbitmap('Ura.ico')
    win2.title('Options')
    win2.focus_set()

    ## format_frame ################################
    format_frame = LabelFrame(win2, text='Format', relief='groove', width=450, height=50)
    format_frame.grid(row=0, column=0, columnspan=2, padx=5)
    format_frame.grid_propagate(False)

    r1 = Radiobutton(format_frame, text=' uu:mm:ss ', variable=format1, value='%H:%M:%S')
    r1.grid(row=0, column=1)
    r2 = Radiobutton(format_frame, text=' uu:mm ', variable=format1, value='%H:%M')
    r2.grid(row=0, column=2)
    if format1.get() == '%H:%M':
        r2.select()
    else:
        r1.select()

    ## position_frame ################################
    position_frame = LabelFrame(win2, text='Pozicija', relief='groove', width=450, height=50)
    position_frame.grid(row=1, column=0, columnspan=2)
    position_frame.grid_propagate(False)

    Label(position_frame, text='x: ').grid(row=0, column=0, padx=(5, 0))
    Entry(position_frame, textvariable=x1, width=4).grid(row=0, column=1, padx=(0, 20))
    Label(position_frame, text='y: ').grid(row=0, column=2)
    Entry(position_frame, textvariable=y1, width=4).grid(row=0, column=3)

    ## color_frame ################################
    color_frame = LabelFrame(win2, text='Barva', relief='groove', width=450, height=50)
    color_frame.grid(row=2, column=0, columnspan=2)
    color_frame.grid_propagate(False)

    Button(color_frame, text='Barva napisa', command=lambda arg=1: get_color(arg)).grid(row=0, column=0, padx=(5, 0))
    l1 = Label(color_frame, text='     ', bg=color1)
    l1.grid(row=0, column=1, padx=(5, 20))
    Button(color_frame, text='Barva ozadja', command=lambda arg=2: get_color(arg)).grid(row=0, column=2)
    l2 = Label(color_frame, text='     ', bg=color2)
    l2.grid(row=0, column=3, padx=(5, 20))
    Button(color_frame, text='Barva alarma', command=lambda arg=3: get_color(arg)).grid(row=0, column=4)
    l3 = Label(color_frame, text='     ', bg=color3)
    l3.grid(row=0, column=5, padx=(5, 20))

    ## font_frame ################################
    font_frame = LabelFrame(win2, text='Pisava', relief='groove', width=450, height=50)
    font_frame.grid(row=4, column=0, columnspan=2)
    font_frame.grid_propagate(False)

    Button(font_frame, text='Izbor pisave', command=choose_font).grid(row=0, column=0, padx=(5, 10))
    Label(font_frame, text='Velikost: ').grid(row=0, column=1)
    v = Entry(font_frame, width=4)
    v.grid(row=0, column=2)
    v.insert(0, str(size))

    ## misc_frame ################################
    misc_frame = LabelFrame(win2, text='Misc', relief='groove', width=450, height=50)
    misc_frame.grid(row=5, column=0, columnspan=2)
    misc_frame.grid_propagate(False)

    Checkbutton(misc_frame, text='Premikanje z miško', variable=move1, command=move_fnc).grid(row=0, column=0)
    Checkbutton(misc_frame, text='Vedno na vrhu', variable=ontop1, command=ontop_fnc).grid(row=0, column=1)

    ## alarm_frame ################################
    alarm_frame = LabelFrame(win2, text='Alarm', relief='groove', width=450, height=200)
    alarm_frame.grid(row=6, column=0, columnspan=2)
    alarm_frame.grid_propagate(False)

    rad_var = IntVar()
    rad_var.set(beep)

    def sel():
        global beep
        beep = rad_var.get()
        if beep:
            e3.config(state=DISABLED)
            e4.config(state=DISABLED)
        else:
            e3.config(state=NORMAL)
            e4.config(state=NORMAL)

    r_frame = Frame(alarm_frame)
    r_frame.grid(row=0, column=0, columnspan=2)
    Radiobutton(r_frame, text=' Simple beep ', variable=rad_var, value=1, command=sel).grid(row=0, column=0)
    Radiobutton(r_frame, text=' Song ', variable=rad_var, value=0, command=sel).grid(row=0, column=1)

    def browse(x):
        global file, player
        openfilename = filedialog.askopenfilename(filetypes=[("all files", "*")])
        if x:
            if openfilename:
                e4_var.set(openfilename)
                player = openfilename
        else:
            if openfilename:
                e3_var.set(openfilename)
                file = openfilename

    Label(alarm_frame, text='Song location\n(eg. C:/music/song3.mp3)', justify=LEFT).grid(row=1, column=0, sticky='w',
                                                                                          padx=(5, 0))

    e3 = Entry(alarm_frame, textvariable=e3_var, width=60)
    e3.grid(row=3, column=0, padx=(5, 0))
    Button(alarm_frame, text='Prebrskaj', command=lambda arg=0: browse(arg)).grid(row=3, column=1, padx=(5, 0))

    Label(alarm_frame,
          text='Player location\n(eg. C:/Program Files (x86)/Windows Media Player/wmplayer.exe,\nIf empty, then the default player is used.)',
          justify=LEFT).grid(row=4, column=0, sticky='w', padx=(5, 0))

    e4 = Entry(alarm_frame, textvariable=e4_var, width=60)
    e4.grid(row=6, column=0, padx=(5, 0))
    Button(alarm_frame, text='Prebrskaj', command=lambda arg=1: browse(arg)).grid(row=6, column=1, padx=(5, 0))
    sel()

    ## ostalo ##################################
    buttons_frame = Frame(win2)
    buttons_frame.grid(row=7, column=1, sticky='e', padx=5, pady=5)

    Button(buttons_frame, text='Izhod', command=save_close, width=7).grid(row=20, column=3)
    Button(buttons_frame, text='Uporabi', command=uporabi, width=7).grid(row=20, column=4, padx=3)
    Button(buttons_frame, text='V redu', command=v_redu, width=7).grid(row=20, column=5)

    def _delete_window():
        global win2
        try:
            win2.destroy()
            win2 = None
        except:
            pass

    win2.protocol('WM_DELETE_WINDOW', _delete_window)
    win2.bind_all('<Return>', uporabi)


help_text = ['"o"', '- options', '"Middle mouse button"', '- options', '"a"', '- set alarm', '"Right mouse button"',
             '- set alarm', '"Double left mouse button"', '- start alarm']


def help_window(*args):
    global win3
    if win3:
        return 0  # prevent more than 1 help window
    win3 = Toplevel(root)
    win3.iconbitmap('Ura.ico')
    win3.title('Ura - Help')
    win3.focus_set()

    for j, i in enumerate(help_text):
        Label(win3, text=i, justify=LEFT).grid(row=j // 2, column=j % 2, sticky='w')

    def _delete_window():
        global win3
        try:
            win3.destroy()
            win3 = None
        except:
            pass

    win3.protocol('WM_DELETE_WINDOW', _delete_window)


def loop():
    global alarm_active, alarm, beep, file
    root.after(980, loop)
    now = strftime(format1.get(), localtime())
    curr_time.set(now)
    if alarm_active:
        if now[:5] == alarm:
            if beep:
                Beep(400, 200)
            else:
                alarm_set()
                if player:
                    a1 = player.split('/')
                    loc = ''
                    for i in a1[:-1]: loc = loc + i + '/'
                    os.system('start /d "' + loc[:-1] + '" ' + a1[-1] + ' "' + file + '"')
                else:
                    os.startfile(file)
        else:
            pass


loop()

root.bind('<Double-Button-1>', alarm_set)
root.bind('<Button-3>', alarm_window)
##root.bind('<Button-3>', save_close)
root.bind('<Button-2>', options_window)
root.bind_all('o', options_window)
root.bind_all('a', alarm_window)
root.bind_all('<F1>', help_window)

root.mainloop()
