import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import *
import tkinter.ttk as ttk
import numpy as np
import time


class Integral:
    def __init__(self, a, b, epsmin, epsmax, step, func):
        """
            Вычисление определенных интегралов численными методами
            :param a: левый предел интегрирования (float)
            :param b: правый предел интегрирования (float)
            :param epsmin: минимальная погрешность вычисления (float)
            :param epsmax: максимальная погрешность вычисления (float)
            :param step: шаг сканирования (float)
            :param func: вычисляемая функция (str)
        """
        self.func = func
        self.a = a
        self.b = b
        self.epsmin = epsmin
        self.epsmax = epsmax
        self.step = step
        self.eps = 0

    def function(self, x):
        exec("x={}\nres={}".format(x, self.func))
        return locals()['res']

    def Metod_Levych_Pryamougolnikov(self, a, b, eps):
        n = 0
        s = 0
        while True:
            n += 2
            s1 = s
            h = (b - a) / n
            s = 0
            xb = a
            for i in range(1, n):
                x = xb + i * h
                s = s + self.function(x) * h
            if abs(s - s1) <= eps:
                break
        return n, s

    def Metod_Srednich_Pryamougolnikov(self, a, b, eps):
        n = 0
        s = 0
        while True:
            n += 2
            s1 = s
            h = (b - a) / n
            s = 0
            xb = a + h / 2
            for i in range(n):
                x = xb + i * h
                s = s + self.function(x) * h
            if abs(s - s1) <= eps:
                return n, s

    def Metod_Pravych_Pryamougolnikov(self, a, b, eps):
        n = 0
        s = 0
        while True:
            n += 2
            s1 = s
            h = (b - a) / n
            s = 0
            xb = a
            for i in range(1, n + 1):
                x = xb + i * h
                s = s + self.function(x) * h
            if abs(s - s1) <= eps:
                return n, s

    def Metod_Trapeciy(self, a, b, eps):
        n = 0
        s = 0
        while True:
            n += 2
            s1 = s
            h = (b - a) / n
            s = (self.function(a) + self.function(b)) / 2
            for i in range(1, n):
                x = a + i * h
                s = s + self.function(x)
            s = s * h
            if abs(s - s1) <= eps:
                return n, s

    def Metod_Parabol(self, a, b, eps):
        global s
        n = 0
        s = 0
        while True:
            n += 2
            s1 = s
            h = (b - a) / n
            s = self.function(a) + self.function(b)
            for i in range(1, n):
                x = a + i * h
                if i % 2 == 0:
                    s = s + 2 * self.function(x)
                else:
                    s = s + 4 * self.function(x)
            s = s * h / 3
            if abs(s - s1) <= eps:
                return n, s

    def run(self):
        """
        Функция формирования отчета вычислений
        :return:
        """
        try:
            if not self.a < self.b:
                raise ValueError("Неверно задан диапазон интегрирования!")
        except ValueError as err:
            return 0, 0, err

        try:
            if not self.epsmin < self.epsmax:
                raise ValueError("Неверно задан диапазон погрешностей!")
        except ValueError as err:
            return 0, 0, err

        self.eps = self.epsmin

        result_lst.insert(INSERT, 'ВЫЧИСЛЕНИЕ ОПРЕДЕЛЕННЫХ ИНТЕГРАЛОВ\nИТЕРАЦИЯ - 1\n')
        for_graph = {"mlp": [], "msp": [], "mrp": [], "mt": [], "mp": []}

        progress_bar_length = round((self.epsmax - self.epsmin) / self.step)
        progress_bar['value'] = 0

        iterate = 1

        while True:
            try:
                result_lst.insert(INSERT, 'Метод левых прямоугольников\n')
                n, s, = self.Metod_Levych_Pryamougolnikov(self.a, self.b, self.eps)
                result_lst.insert(INSERT, '   n={}, s={:.5f} eps={:.5f}\n'.format(n, s, self.eps))
                for_graph['mlp'].append(n)

                progress_bar_plus(progress_bar_length)

                result_lst.insert(INSERT, 'Метод средних прямоугольников\n')
                n, s = self.Metod_Srednich_Pryamougolnikov(self.a, self.b, self.eps)
                result_lst.insert(INSERT, '   n={}, s={:.5f} eps={:.5f}\n'.format(n, s, self.eps))
                for_graph['msp'].append(n)

                progress_bar_plus(progress_bar_length)

                result_lst.insert(INSERT, 'Метод правых прямоугольников\n')
                n, s = self.Metod_Pravych_Pryamougolnikov(self.a, self.b, self.eps)
                result_lst.insert(INSERT, '   n={}, s={:.5f} eps={:.5f}\n'.format(n, s, self.eps))
                for_graph['mrp'].append(n)

                progress_bar_plus(progress_bar_length)

                result_lst.insert(INSERT, 'Метод трапеций\n')
                n, s = self.Metod_Trapeciy(self.a, self.b, self.eps)
                result_lst.insert(INSERT, '   n={}, s={:.5f} eps={:.5f}\n'.format(n, s, self.eps))
                for_graph['mt'].append(n)

                progress_bar_plus(progress_bar_length)

                result_lst.insert(INSERT, 'Метод парабол\n')
                n, s = self.Metod_Parabol(self.a, self.b, self.eps)
                result_lst.insert(INSERT, '   n={}, s={:.5f} eps={:.5f}\n'.format(n, s, self.eps))
                for_graph['mp'].append(n)

                progress_bar_plus(progress_bar_length)

                self.eps = self.eps + self.step
            except Exception as err:
                return 0, 0, err

            if self.eps > self.epsmax:
                result_lst.insert(INSERT, '\n\nВЫЧИСЛЕНИЯ ОКОНЧЕНЫ')
                progress_bar_plus(progress_bar_length, end=True)
                run_button['state'] = 'normal'
                run_button.bind('<Button-1>', run)
                return for_graph, 0
            else:
                iterate += 1
                result_lst.insert(INSERT, '\n\nСЛЕДУЮЩАЯ ИТЕРАЦИЯ - {}\n\n'.format(iterate))


def window_size():
    """Функция форматирования размеров окна приложения"""
    w = 1100
    h = 600
    return "{}x{}".format(w, h)


def help_window():
    """
    Функция инициализации окна справки
    """
    help_root = Toplevel()
    help_root.geometry("500x500")
    help_root.resizable(0, 0)
    help_root.title('Справка')
    txt = """
            fabs(X) или abs(x) - модуль X.\n
            factorial(X) - факториал числа X.\n
            fmod(X, Y) или (X % Y) - остаток от деления X на Y.\n
            exp(X) - eX.\n
            log(X, [base]) - логарифм X по основанию base.\n         Если base не указан, вычисляется натуральный логарифм.\n
            log1p(X) - натуральный логарифм (1 + X).\n
            log10(X) - логарифм X по основанию 10.\n
            log2(X) - логарифм X по основанию 2.\n
            sqrt(X) - квадратный корень из X.\n
            X**Y - возведение X в степень Y.\n
            acos(X) - арккосинус X. В радианах.\n
            asin(X) - арксинус X. В радианах.\n
            atan(X) - арктангенс X. В радианах.\n
            cos(X) - косинус X (X указывается в радианах).\n
            sin(X) - синус X (X указывается в радианах).\n
            tan(X) - тангенс X (X указывается в радианах).\n
            hypot(X, Y) - вычисляет гипотенузу треугольника\n          с катетами X и Y (sqrt(x * x + y * y)).\n
            degrees(X) - конвертирует радианы в градусы.\n
            radians(X) - конвертирует градусы в радианы.\n
            cosh(X) - вычисляет гиперболический косинус.\n
            sinh(X) - вычисляет гиперболический синус.\n
            tanh(X) - вычисляет гиперболический тангенс.\n
            acosh(X) - вычисляет обратный гиперболический косинус.\n
            asinh(X) - вычисляет обратный гиперболический синус.\n
            atanh(X) - вычисляет обратный гиперболический тангенс.\n
            pi - pi = 3,1415926...\n
            e - e = 2,718281...\n\n
            Интерфейс подготовил: Поленок Вячеслав\n
            Версия: 0.1
            """
    help_scrollbar = Scrollbar(help_root)
    help_scrollbar.pack(side=RIGHT, fill=Y, padx=3)

    text = Text(help_root, font='arial 12', yscrollcommand=help_scrollbar.set)
    text.place(x=0, y=0, height=500, width=480)
    text.insert(INSERT, txt)
    help_scrollbar.config(command=text.yview)

    help_root.mainloop()


def clear():
    """Функция сброса введенных значений и отчета вычислений"""
    result_lst.delete('1.0', END)
    ax.cla()
    root.update()
    size = root.geometry().split('x')
    size[0] = str(int(size[0]) - 1)
    s = "x".join(size)
    root.geometry(s)
    canvas.show()


def init_graph():
    """
    Функция инициализации поля графиков
    """
    ax.set_title("Количество итераций для разной погрешности")
    ax.set_xlabel("Погрешность")
    ax.set_ylabel("Количество итераций")
    ax.grid(which='both')


def progress_bar_plus(progress_bar_length, end=0):
    """
    Функция обновления прогресс бара
    :param progress_bar_length: длинна прогресс бара
    :param end: параметр заполнения прогресс бара
    """
    progress_step = round(100 / progress_bar_length / 5, 5)
    if progress_bar['value'] + progress_step > 100:
        progress_bar['value'] = 100
    if end is True:
        progress_bar['value'] = 100
    else:
        progress_bar.step(progress_step)
    status['text'] = "Выполнено: {}%".format(round(progress_bar['value']))
    root.update()
    time.sleep(0.0001)


def run():
    """
    Функция обработки пользовательского ввода
    """
    clear()
    progress_bar['value'] = 0
    try:
        a = float(Entry.get(l_diapason_input))
        b = float(Entry.get(r_diapason_input))
        epsmin = float(Entry.get(l_eps_input))
        epsmax = float(Entry.get(r_eps_input))
        step = float(Entry.get(step_input))
        func = Entry.get(func_input)
        run_button['state'] = 'disabled'
        run_button.bind('<Button-1>', stopper)
        integr = Integral(a, b, epsmin, epsmax, step, func)
        for_graph, errors = integr.run()

        if errors != 0:
            result_lst.insert(INSERT, errors)

        x = np.arange(epsmin, epsmax, step)

        init_graph()

        ax.plot(x, for_graph['mlp'], 'r', linewidth=1, label="Метод Левых прямоугольников", marker=".")
        ax.plot(x, for_graph['msp'], 'g', linewidth=1, label="Метод Средних прямоугольников", marker=".")
        ax.plot(x, for_graph['mrp'], 'b', linewidth=1, label="Метод Правых прямоугольников", marker=".")
        ax.plot(x, for_graph['mt'], 'y', linewidth=1, label="Метод Трапеций", marker=".")
        ax.plot(x, for_graph['mp'], 'c', linewidth=1, label="Метод Парабол", marker=".")
        # Легенда
        ax.legend()
        canvas.show()
    except ValueError as err:
        result_lst.insert(INSERT, "Не указаны или неверно указаны исходные данные!")


root = Tk()
root.title("Интеграл")
root.geometry(window_size())

menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu)
menu.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Очистить", command=clear)
file_menu.add_command(label="Выход", command=root.destroy)
help_menu = Menu(menu)
menu.add_cascade(label="Справка", menu=help_menu)
help_menu.add_command(label="Список функций", command=help_window)

# ввод функции
frame = Frame(root)
frame.pack(fill=BOTH, expand=1)

func_input_lable = Label(frame, text="Введите функцию :")
func_input_lable.place(x=8, y=10, width=110)

func_input = Entry(frame)
func_input.place(x=120, y=10, width=220, height=25)
func_input.insert(0, '1/(1+x**2)')

run_button = Button(frame, text="Вычислить")
run_button.bind("<Button-1>", run)

run_button.place(x=350, y=10, width=80)

# ввод диапазона
diapason_frame = Frame(frame)
diapason_frame.place(x=15, y=40, width=240, height=50)

diapason_input_lable = Label(diapason_frame, text="Предел интегрирования :")
diapason_input_lable.place(x=0, y=0, width=140)

l_diapason_labele = Label(diapason_frame, text="[", font='Arial 15')
l_diapason_labele.place(x=25, y=20, width=5)

l_diapason_input = Entry(diapason_frame)
l_diapason_input.place(x=35, y=26, width=30, height=20)
l_diapason_input.insert(0, '1')

c_diapason_labele = Label(diapason_frame, text=";", font='Arial 15')
c_diapason_labele.place(x=65, y=20, width=5)

r_diapason_input = Entry(diapason_frame)
r_diapason_input.place(x=75, y=26, width=30, height=20)
r_diapason_input.insert(0, '2')

r_diapason_labele = Label(diapason_frame, text="]", font='Arial 15')
r_diapason_labele.place(x=110, y=20, width=5)

# ввод погрешностей
eps_frame = Frame(frame)
eps_frame.place(x=160, y=40, width=240, height=50)

eps_input_lable = Label(eps_frame, text="Погрешности [min ; max] :")
eps_input_lable.place(x=15, y=0, width=145)

l_eps_labele = Label(eps_frame, text="[", font='Arial 15')
l_eps_labele.place(x=25, y=20, width=5)

l_eps_input = Entry(eps_frame)
l_eps_input.place(x=35, y=26, width=45, height=20)
l_eps_input.insert(0, '0.0001')

c_eps_labele = Label(eps_frame, text=";", font='Arial 15')
c_eps_labele.place(x=75, y=20, width=5)

r_eps_input = Entry(eps_frame)
r_eps_input.place(x=85, y=26, width=45, height=20)
r_eps_input.insert(0, '0.001')

r_eps_labele = Label(eps_frame, text="]", font='Arial 15')
r_eps_labele.place(x=135, y=20, width=5)

# ввод шага
step_input_lable = Label(eps_frame, text="Шаг :")
step_input_lable.place(x=182, y=0, width=40)

step_input = Entry(eps_frame)
step_input.place(x=190, y=26, width=45, height=20)
step_input.insert(0, '0.0001')
# вывод

result_frame = LabelFrame(frame, text="Результат :", padx=5, pady=5)
result_frame.place(x=10, y=90, width=420, relheight=1.0, height=-100)

scrollbar = Scrollbar(result_frame)
scrollbar.place(anchor="ne", relheight=1.0, height=-25, relx=1.0, x=-3)

result_lst = Text(result_frame, yscrollcommand=scrollbar.set, width=30, height=6)
result_lst.place(x=0, y=0, width=387, relheight=1.0, height=-27)
scrollbar.config(command=result_lst.yview)

progress_bar = ttk.Progressbar(result_frame, orient='horizontal', mode='determinate')
progress_bar.place(height=22, relwidth=1.0, width=-110, rely=1.0, y=-23)

status = Label(result_frame, text="Готов", anchor='center')
status.place(x=305, rely=1.0, y=-23, width=100)
# график

canvas_frame = LabelFrame(frame, text="График :", padx=5, pady=5)
canvas_frame.place(x=445, y=5, relwidth=1.0, width=-460, relheight=1.0, height=-15)

fig, ax = plt.subplots()

init_graph()

canvas = FigureCanvasTkAgg(fig, canvas_frame)
canvas.show()
canvas.get_tk_widget().place(x=0, y=0, width=1, height=1)
toolbar = NavigationToolbar2TkAgg(canvas, canvas_frame)

toolbar.update()
canvas._tkcanvas.place(x=0, y=0, relwidth=1.0, width=-5, relheight=1.0, height=-35)

root.bind("<Return>", run)

root.mainloop()
