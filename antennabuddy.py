import ttkbootstrap as ttk
from time import sleep
# import tkinter as tk
import serial
import serial.tools.list_ports as ports

ports_available = []
ser = serial.Serial()
is_serial_open = False


def azimuth_plus():
    if is_serial_open:
        ser.write(b"#1\n")


def azimuth_minus():
    if is_serial_open:
        ser.write(b"#2\n")


def elevation_plus():
    if is_serial_open:
        ser.write(b"#3\n")


def elevation_minus():
    if is_serial_open:
        ser.write(b"#4\n")


def scan_ports():
    ports_available.clear()
    for port in ports.comports():
        ports_available.append(port.name)


window = ttk.Window(themename="darkly")
window.title("Antenna Callibrator")
window.geometry("600x430")
window.maxsize(600, 430)


title_label = ttk.Label(master=window, text="Antenna Buddy", font="Calibri 24 bold")
title_label.pack(side="top")

frame1 = ttk.Frame(window)
frame1.pack(pady=20)


azimuth_label = ttk.Label(master=frame1, text="Azimuth Angle  ", font="Times 15")
azimuth_label.pack(side="left")

azmuth_minus_button = ttk.Button(
    master=frame1, text="-", bootstyle="primary", width=8, command=azimuth_minus
)
azmuth_minus_button.pack(side="left", padx=10)

azmuth_plus_button = ttk.Button(master=frame1, text="+", width=8, command=azimuth_plus)
azmuth_plus_button.pack(side="left")

frame2 = ttk.Frame(window)
frame2.pack(pady=20)

elevation_label = ttk.Label(master=frame2, text="Elevation Angle", font="Times 15")
elevation_label.pack(side="left")

elevation_minus_button = ttk.Button(
    master=frame2, text="-", width=8, command=elevation_minus)
elevation_minus_button.pack(side="left", padx=9)

elevation_plus_button = ttk.Button(
    master=frame2, text="+", width=8, command=elevation_plus)
elevation_plus_button.pack(side="left")

frame3 = ttk.Frame(window)
frame3.pack(pady=20)

com_label = ttk.Label(master=frame3, text="Port", font="Times 15")
com_label.pack(side="left", padx=10)
# port_variable = ttk.StringVar()
com_ports_menu = ttk.Combobox(
    frame3, state="readonly", values=ports_available, postcommand=scan_ports()
)
# com_ports_menu.bind('<<ComboboxSelected>>', on_select)
try:
    com_ports_menu.current(0)
except:
    pass

com_ports_menu.pack(side="left", padx=5)

baudrate_list = ["4800", "9600", "115200"]
baudrate_menu = ttk.Combobox(frame3, state="readonly", values=baudrate_list)
baudrate_menu.current(1)
baudrate_menu.pack(padx=5)

frame4 = ttk.Frame(window)
frame4.pack(pady=20)


def update_ports():
    scan_ports()
    com_ports_menu["values"] = ports_available
    try:
        com_ports_menu["state"] = "readonly"
        com_ports_menu.current(0)
    except:
        com_ports_menu["state"] = "disabled"


scan_button = ttk.Button(frame4, bootstyle="info", text="Scan", command=update_ports)
scan_button.pack(side="right")

is_on = False
# close_button_style = ttk.Style()
# close_button_style.configure("danger", background="red")


def bind_serial():
    global is_on
    global is_serial_open
    if is_on == False and len(ports_available) != 0:
        ser.port = com_ports_menu.get()
        ser.baudrate = baudrate_menu.get()
        ser.open()
        # print(ser.port)
        # print(ser.baudrate)
        start_serial["text"] = "Close"
        is_on = not is_on
        is_serial_open = True
        sleep(2)
        ser.write(b"x\n")
        baudrate_menu["state"] = "disabled"
        com_ports_menu["state"] = "disabled"
        scan_button["state"] = "disabled"


    else:
        ser.close()
        is_on = not is_on
        is_serial_open = False
        start_serial["text"] = "Open Port"
        baudrate_menu["state"] = "readonly"
        com_ports_menu["state"] = "readonly"
        scan_button["state"] = "readonly"

start_serial = ttk.Button(
    frame4, bootstyle="danger", text="Open Port", command=bind_serial
)
start_serial.pack(side="right", padx=20)

frame5 = ttk.Frame(window)
frame5.pack()
note_label = ttk.Label(frame5, text="Note: This software is developed for research and study of \"Design And \nDevelopment Of Ground Station, ML Model and IOT Monitoring Platform\n For Weather Forecasting\", The Final Year Project of Students of nec")
note_label.pack()
final_label = ttk.Label(frame5, text="Department of Electronics And Communication")
final_label.pack()


window.mainloop()
