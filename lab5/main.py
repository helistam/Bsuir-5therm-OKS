import functools
from tkinter import *
from tkinter import scrolledtext, ttk

import Reader
import Sender

global comboboxs1,comboboxs2,comboboxs3,SendAdress,debug_text
SendAdress=0
debug_text=0
def generate_marker():
    # Ваш код для генерации маркера
    print("Генерация маркера")
    Reader.delete_marker=0
    Sender.GenerateMark()

def control_marker(button,win):

    if button==win.get():
        Reader.delete_marker=1
        print("Контроль маркера")
    else:
        debug_text.insert(INSERT, "Данная станция не является главной\n")


def prevent_loops():
    # Ваш код для предотвращения циклов
    print("Предотвращение циклов")

def chooseStation1(event):
    global SendAdress
    selection = comboboxs1.get()
    if selection=="Станция2":
        SendAdress=2
    else:
        if selection=="Станция3":
            SendAdress=3
def chooseStation2(event):
    global SendAdress
    selection = comboboxs2.get()
    if selection=="Станция1":
        SendAdress=1
    else:
        if selection=="Станция3":
            SendAdress=3
def chooseStation3(event):
    global SendAdress
    selection = comboboxs3.get()
    if selection=="Станция1":
        SendAdress=1
    else:
        if selection=="Станция2":
            SendAdress=2
    print(selection)

def choose_ports(text,current_station):
    global comboboxs
    if current_station==1:
        list_of_ports = ["Станция2", "Станция3"]
    else:
        if current_station==2:
            list_of_ports = ["Станция1", "Станция3"]
        else:
            if current_station==3:
                list_of_ports = ["Станция1", "Станция2"]
    return list_of_ports


def on_priority_change(event,window_addr):
    print(f"window_addr={window_addr}")
    if window_addr==1:
        selected_priority = priority_combobox.get()
        if selected_priority == "Priority 1":
            Sender.priority1 = 1
            Sender.priority = 1
        elif selected_priority == "Priority 2":
            Sender.priority = 2
            Sender.priority1 = 2
    if window_addr==2:
        selected_priority = priority_combobox2.get()
        if selected_priority == "Priority 1":
            Sender.priority = 1
            Sender.priority2 = 1
        elif selected_priority == "Priority 2":
            Sender.priority = 2
            Sender.priority2 = 2
    if window_addr==3:
        selected_priority = priority_combobox3.get()
        if selected_priority == "Priority 1":
            Sender.priority=1
            Sender.priority3 = 1
        elif selected_priority == "Priority 2":
            Sender.priority = 2
            Sender.priority3 = 2

def clear_debug_text():
    debug_text.delete("1.0", "end")

def GUI():#функция для User interface


    global comboboxs1, comboboxs2, comboboxs3,SendAdress,debug_text,priority_combobox,priority_combobox2,priority_combobox3
    root = Tk()
    root.title("Приложение на Tkinter")
    root.geometry("1200x600")

    main_station_var = IntVar()
    main_station_var.set(1)

    # Создаем и добавляем три фрейма в окно
    frame1 = Frame(root, width=400, height=600, relief=SUNKEN, bd=2)
    frame2 = Frame(root, width=400, height=600, relief=SUNKEN, bd=2)
    frame3 = Frame(root, width=400, height=600, relief=SUNKEN, bd=2)

    frame1.pack(side=LEFT, fill=BOTH, expand=True)
    frame2.pack(side=LEFT, fill=BOTH, expand=True)
    frame3.pack(side=LEFT, fill=BOTH, expand=True)

    window = Toplevel()
    window.title("Отладочное окно ")
    window.geometry("540x540")
    debug_text = scrolledtext.ScrolledText(window, width=60, height=25)
    debug_text.pack(pady=10)

    clear_button = Button(window, text="Очистить", command=clear_debug_text)
    clear_button.pack()

    # Пример текстовой метки в каждом фрейме
    label1 = Label(frame1, text="Станция 1")
    label1.pack()
    label2 = Label(frame1, text="COM7 COM8")
    label2.pack()
    label7 = Label(frame1, text="COM7")
    label8 = Label(frame1, text="")
    label7.place(x=150, y=45)
    label9 = Label(frame1, text="COM8")
    txt78 = scrolledtext.ScrolledText(frame1,width=30, height=5)
    text = Entry(frame1, width=25)
    label8.pack()
    label9.place(x=300, y=40)
    txt78.pack(anchor=W)
    text.place(x=245, y=70)
    text.bind("<Return>", lambda e, f=text, sendAdress=lambda: SendAdress: Sender.Send_func(e, f, sendAdress(),1))

    comboboxs1 = ttk.Combobox(frame1, values= choose_ports(frame1,1))
    comboboxs1.place(x=140, y=180)
    comboboxs1.bind("<<ComboboxSelected>>", chooseStation1)
    Reader.readfunc(txt78,1,debug_text)

    rb1 = Radiobutton(frame1, text="Главная станция", variable=main_station_var, value=1)
    rb1.place(x=140, y=220)

    btn_generate_marker1 = Button(frame1, text="Генерировать маркер", command=generate_marker)
    btn_generate_marker1.place(x=140, y=250)

    btn_control_marker1 = Button(frame1, text="Удалить маркер", command=lambda: control_marker(1,main_station_var))
    btn_control_marker1.place(x=140, y=280)


    priority_combobox = ttk.Combobox(frame1, values=["Priority 1", "Priority 2"])
    priority_combobox.set("Priority 1")  # Default value
    priority_combobox.place(x=140, y=410)

    priority_combobox.bind("<<ComboboxSelected>>", lambda event: on_priority_change(event, window_addr=1))


    label3 = Label(frame2, text="Станция 2")
    label3.pack()
    label4 = Label(frame2, text="COM9 COM10")
    label4.pack()
    label7 = Label(frame2, text="COM9")
    label8 = Label(frame2, text="")
    label7.place(x=150, y=45)
    label9 = Label(frame2, text="COM10")
    txt910 = scrolledtext.ScrolledText(frame2,width=30, height=5)
    text = Entry(frame2, width=25)
    label8.pack()
    label9.place(x=300, y=40)
    txt910.pack(anchor=W)
    text.place(x=245, y=70)
    text.bind("<Return>", lambda e, f=text, sendAdress=lambda: SendAdress: Sender.Send_func(e, f, sendAdress(),2))

    comboboxs2 = ttk.Combobox(frame2, values=choose_ports(frame2, 2))
    comboboxs2.place(x=140, y=180)
    comboboxs2.bind("<<ComboboxSelected>>", chooseStation2)
    Reader.readfunc(txt910,2,debug_text)

    rb2 = Radiobutton(frame2, text="Главная станция", variable=main_station_var, value=2)
    rb2.place(x=140, y=220)

    btn_generate_marker2 = Button(frame2, text="Генерировать маркер", command=generate_marker)
    btn_generate_marker2.place(x=140, y=250)

    btn_control_marker2 = Button(frame2, text="Удалить маркер", command=lambda: control_marker(2,main_station_var))
    btn_control_marker2.place(x=140, y=280)


    priority_combobox2 = ttk.Combobox(frame2, values=["Priority 1", "Priority 2"])
    priority_combobox2.set("Priority 1")  # Default value
    priority_combobox2.place(x=140, y=410)

    priority_combobox2.bind("<<ComboboxSelected>>", lambda event: on_priority_change(event, window_addr=2))

    label5 = Label(frame3, text="Станция 3")
    label5.pack()
    label6 = Label(frame3, text="COM11 COM12")
    label6.pack()
    label7 = Label(frame3, text="COM11")
    label8 = Label(frame3, text="")
    label7.place(x=150, y=45)
    label9 = Label(frame3, text="COM12")
    txt = scrolledtext.ScrolledText(frame3,width=30, height=5)
    text = Entry(frame3, width=25)
    label8.pack()
    label9.place(x=300, y=40)
    txt.pack(anchor=W)
    text.place(x=245, y=70)
    text.bind("<Return>", lambda e, f=text, sendAdress=lambda: SendAdress: Sender.Send_func(e, f, sendAdress(),3))

    comboboxs3 = ttk.Combobox(frame3, values=choose_ports(frame3, 3))
    comboboxs3.place(x=140, y=180)
    comboboxs3.bind("<<ComboboxSelected>>", chooseStation3)
    Reader.readfunc(txt,3,debug_text)

    rb3 = Radiobutton(frame3, text="Главная станция", variable=main_station_var, value=3)
    rb3.place(x=140, y=220)

    btn_generate_marker3 = Button(frame3, text="Генерировать маркер", command=generate_marker)
    btn_generate_marker3.place(x=140, y=250)

    btn_control_marker3 = Button(frame3, text="Удалить маркер", command=lambda: control_marker(3,main_station_var))
    btn_control_marker3.place(x=140, y=280)


    priority_combobox3 = ttk.Combobox(frame3, values=["Priority 1", "Priority 2"])
    priority_combobox3.set("Priority 1")  # Default value
    priority_combobox3.place(x=140, y=410)

    priority_combobox3.bind("<<ComboboxSelected>>", lambda event: on_priority_change(event, window_addr=3))


    root.mainloop()

GUI()