

import threading
from tkinter import *
from tkinter import messagebox
import customtkinter
import mido
from stupidArtnet import StupidArtnetServer
import time
from datetime import datetime
from threading import Thread
import rtmidi

#customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
#customtkinter.set_default_color_theme("theme\costom.json")
root = customtkinter.CTk()
root.title("ArtnetMidi")
root.geometry("1240x760")
root.config(background="#125276")


used_list = []
midi_ports = []



def select_device():
    global select_enhed
    global artnet
    select_enhed = device_listbox.get(ANCHOR)
    device_label.configure(text=select_enhed)
    artnet = artnet_universe.get()
    artnet_universe_label.configure(text="Universe: "+ artnet)


def start():
    try:
        global logView
        global textbox
        global thread
        global stop_threads
        print(used_check.get())
        # get input
        stop_threads = False
        thread = Thread(target = run, args = (select_enhed, artnet, ))
        thread.start()
        info_label.configure(text="RUNNING")
    except:
        messagebox.showerror("Error", "Midi device or Artnet input not Select")
        pass


def get():
    midiout = rtmidi.MidiOut()
    device_info = midiout.get_ports()
    for item in device_info:
        #midi_ports.append(item)
        device_listbox.insert(0, item)
    #device_listbox.configure(values=midi_ports)
    root.update()


def run(name, artnet):
    global dt
    # logbook - start
    dt = datetime.now()
    print(dt)
    with open("log.txt", "w") as f:
        f.write(f"{dt}\n")



    def test_callback(data):

        send_midi(data)

    def send_midi(data):
        usedValue = used_check.get()
        dmx_ch = len(data)

        if usedValue == "on":
            for x in range(dmx_ch):
                if data[x] > 127 and x not in used_list:
                    print("DMX CH", x+1, " is not in used_list")
                    outport = mido.open_output(name)
                    outport.send(mido.Message('note_on', note=x + 1, velocity=100))
                    print("Midi sent - NoteOn=", x+1)
                    used_list.append(x)
                    print(used_list)
                    with open("Log.txt", "a") as file:
                        file.write(f"{dt} - Note: {x+1}  - DMX CH: {x+1} - DMX Value: {data[x]}\n")
                if data[x] < 127 and data[x] in used_list:
                    #print(data[x], " in used_list")
                    pass

        if usedValue == "off":
            for x in range(dmx_ch):
                new_value = data[x]
                while new_value != old_value:
                    if data[x] > 127:
                        print("DMX Value", data[x])
                        outport = mido.open_output(name)
                        outport.send(mido.Message('note_on', note=x+1, velocity = 100))
                        print("Midi sent - NoteOn=", x+1)
                        with open("Log.txt", "a") as file:
                            file.write(f"{dt} - Note: {x + 1}  - DMX CH: {x + 1} - DMX Value: {data[x]}\n")
                        old_value = data[x]
                    if data[x] < 127:
                        pass





    # You can use universe only
    #print(artnet)
    universe = int(artnet)
    a = StupidArtnetServer()

    u1_listener = a.register_listener(
        universe, callback_function=test_callback)

    while True:
        try:
            # print object state
            #print(a)
            global stop_threads
            if stop_threads:
                thread.join()
                break
            time.sleep(0.2)
        except:
            break


def close():
    global stop_threads
    stop_threads = True
    root.destroy()


def clear_list():
    used_list.clear()
    print("Clear List")
    with open("log.txt", "a") as file:
        file.write(f"Clear liste {dt}\n")







artnet_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]


#text1 = customtkinter.CTkLabel(master=root, text="Artnet to Midi", font=("Helvetica", 30), bg_color="#125276")
#text1.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky=W)

input_del = customtkinter.CTkFrame(master=root, width=300, height=700, border_color="#FFFFFF", border_width=2, fg_color="#125276")
input_del.grid(row=0, column=0, ipady=20, ipadx=20, padx=(10,0), pady=(10,0))
input_del.grid_propagate(False)
setup_del = customtkinter.CTkFrame(master=root, width=500, height=700, border_color="#FFFFFF", border_width=2, fg_color="#125276")
setup_del.grid(row=0, column=1, ipady=20, ipadx=20, pady=(10,0))
setup_del.grid_propagate(False)
info_del = customtkinter.CTkFrame(master=root, width=300, height=700, border_color="#FFFFFF", border_width=2, fg_color="#125276")
info_del.grid(row=0, column=2, ipady=20, ipadx=20, pady=(10,0))
info_del.grid_propagate(False)

input_del.columnconfigure(0, weight=1)
setup_del.columnconfigure(0, weight=1)
info_del.columnconfigure(0, weight=1)

input_del_label = customtkinter.CTkLabel(master=input_del, text="INPUT", font=("Helvetica", 20), bg_color="#125276", text_color="#FFFFFF", )
input_del_label.grid(row=0, column=0,pady=(2,0), padx=2, sticky="enw")
setup_del_label = customtkinter.CTkLabel(master=setup_del, text="SETUP", font=("Helvetica", 20), bg_color="#125276", text_color="#FFFFFF")
setup_del_label.grid(row=0, column=0,pady=(2,0), padx=2, sticky="enw")
info_del_label = customtkinter.CTkLabel(master=info_del, text="INFO", font=("Helvetica", 20), bg_color="#125276", text_color="#FFFFFF")
info_del_label.grid(row=0, column=0,pady=(2,0), padx=2, sticky="enw")


# --------------------------- input del
device_btn = customtkinter.CTkButton(master=input_del, text="MIDI Device", width=200, bg_color="#125276", command=get)
device_btn.grid(row=1, column=0, pady=10, padx=10)

device_listbox = Listbox(input_del, width=45, bg="#125276", fg="#FFFFFF", bd=0)
device_listbox.grid(row=2, column=0, padx=10, pady=10)

#device_listbox = customtkinter.CTkComboBox(master=input_del, values=[""], bg_color="#125276", fg_color="#696969", width=200)
#device_listbox.grid(row=2, column=0, padx=10, pady=10)

artnet_label = customtkinter.CTkLabel(master =input_del, text="Artnet universe:", bg_color="#125276", text_color="#FFFFFF", font=("Helvetica", 20))
artnet_label.grid(row=3, column=0, padx=30, pady=10)

artnet_universe = customtkinter.CTkOptionMenu(master=input_del, bg_color="#125276", values=artnet_list, width=200)
artnet_universe.grid(row=4, column=0, padx=10, pady=10)

# ---------------------------- setup del





select_btn = customtkinter.CTkButton(master=setup_del, text="Select Artnet", width=200, bg_color="#125276", command=select_device)
select_btn.grid(row=3, column=0, padx=0, pady=10)

check_var = customtkinter.StringVar()
used_check = customtkinter.CTkSwitch(master=setup_del, text="Send MIDI Once", bg_color="#125276", variable=check_var, onvalue="on", offvalue="off")
used_check.grid(row=4, column=0, padx=10, pady=10, sticky=W)


device_label = customtkinter.CTkLabel(master=setup_del, text="", bg_color="#125276")
device_label.grid(row=5, column=0, padx=5)

artnet_universe_label = customtkinter.CTkLabel(master=setup_del, text="", bg_color="#125276")
artnet_universe_label.grid(row=6, column=0, padx=5)



# ----------------------------info del

log = customtkinter.CTkButton(master=info_del, text="Clear List", width=200, bg_color="#125276", command=clear_list)
log.grid(row=1, column=0, padx=10, pady=10)

info_label = customtkinter.CTkLabel(master=info_del, text="", bg_color="#125276")
info_label.grid(row=2, column=0, padx=50, pady=5)

start_run = customtkinter.CTkButton(master=info_del, text="Run", width=200, bg_color="#125276", command=start)
start_run.grid(row=4, column=0, padx=10, pady=5)

luk = customtkinter.CTkButton(master=info_del, text="Stop", width=200, bg_color="#125276",  command=close)
luk.grid(row=6, column=0, padx=0, pady=40)






























root.mainloop()
