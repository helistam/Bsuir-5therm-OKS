from tkinter import *
from tkinter import scrolledtext
class Controll:
    global par_value
    par_value="Нечетный"
    def __init__(self, parent, width, height, title="Контроль", resizable=(False, False), icon=None):
        self.root = Toplevel(parent)
        self.root.title(title)

        self.root.geometry(f"{width}x{height}+1000+0")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbimap(icon)

        self.root.title("Форма для выбора варианта проверки паритета")

        # Создаем метку с инструкцией
        label = Label(self.root, text="Выберите вариант проверки паритета:")
        label.pack()

        # Создаем переменную для хранения выбора пользователя
        parity_var = StringVar()

        # Создаем радиокнопки
        parity_even = Radiobutton(self.root, text="Четный паритет", variable=parity_var, value="четный")
        parity_even.pack()

        parity_odd = Radiobutton(self.root, text="Нечетный паритет", variable=parity_var, value="нечетный")
        parity_odd.pack()
        parity_mes = Radiobutton(self.root, text="Нет паритета", variable=parity_var, value="Нет паритета")
        parity_mes.pack()
        parity_mark = Radiobutton(self.root, text="Установка паритета в mark", variable=parity_var, value="Установлен в mark")
        parity_mark.pack()
        parity_space = Radiobutton(self.root, text="Установка паритета в space", variable=parity_var, value="Установлен в space")
        parity_space.pack()
        txt = scrolledtext.ScrolledText(self.root, width=40, height=10)
        txt.pack()
        # Кнопка для подтверждения выбора
        def submit():
            global par_value
            txt.delete(1.0, END)
            par_value = parity_var.get()
            txt.insert(INSERT, par_value)
        submit_button = Button(self.root, text="Подтвердить", command=submit)
        submit_button.pack()



