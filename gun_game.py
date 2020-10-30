from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1200x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
g = 3  # что-то вроде усксорения свободного падения
kv = 0.7  # коэффициент начальной скорости шара
start_r = 45  # start_r и sub_r служат для изменения параметров цели со временем
sub_r = 0
colors = ['blue', 'green', 'red', 'yellow', 'papaya whip']
points = 0
canv_points = canv.create_text(50, 50, text=points, font=("impact", 44))


class Ball:
    def __init__(self, x=40, y=450):
        """ Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        r - радиус мяча
        vx - начальная скорость мяча по горизонтали
        vy - начальная скорость мяча по ветрикали
        live - время жизни
        color - цвет шара
        id - соответсвующая фигура из canv
        global colors - список цветов
        """
        global colors
        self.x = x
        self.y = y
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = choice(colors)
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 50

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        global g
        """Перемещение мяча

        Обновление координаты со временем, обновление скорости мяча и удаление мяча,
        если тот вылетает за нижнюю или правую границу поля. Также удаление шара по времени
        от параметра live, или его уменьшение
        """
        self.x += self.vx
        self.y -= self.vy
        self.vy -= g
        self.set_coords()
        if self.x > 1200 or self.y > 600:
            canv.delete(self.id)
        if self.live < 0:
            balls.pop(balls.index(self))
            canv.delete(self.id)
        else:
            self.live -= 1

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.

        реализована с помощью треугольника с координатами
        (self.x, self.y)
        (self.x - self.vx, self.y - self.vy)
        (obj.x, obj.y)

        a,b,c - стороны треугольника
        p - полупериметр
        s - площадь
        h - высота из вершины с целью(против стороны a)
        r - прицельный параметр (сумма радиусов)
        cosb - косинус против стороны b, умноженный на a*c
        cosc - косинус против стороны c, умноженный на a*b
        """
        a = (self.vx ** 2 + self.vy ** 2) ** 0.5
        c = ((self.x - obj.x) ** 2 +
             (self.y - obj.y) ** 2) ** 0.5
        b = ((self.x - self.vx - obj.x) ** 2
             + (self.y - self.vy - obj.y) ** 2) ** 0.5

        p = (a + b + c)/2
        s = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        h = 2 * s / a
        r = self.r + obj.r
        cosb = (self.x - obj.x) * self.vx + (self.y - obj.y) * self.vy
        cosc = ((self.x - self.vx - obj.x) * (-self.vx)
                + (self.y - self.vy - obj.y)*(-self.vy))
        if ((h < r) and (cosb >= 0) and (cosc >= 0)) or (b < r) or (c < r):
            return True
        else:
            return False


class Gun:
    def __init__(self):
        """
        Инициализация ружья
        """
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=5, arrow=tk.LAST)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        balls - список всех мячей
        bullet_1 - счет мячей на первую цель(обнуляется после попадания)
        bullet_2 - счет мячей на вторую цель(обнуляется после попадания)
        kv - коэффициент начальной скорости шара
        """
        global balls, bullet_1, bullet_2, kv
        bullet_1 += 1
        bullet_2 += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) * kv
        new_ball.vy = - self.f2_power * math.sin(self.an) * kv
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши"""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target:
    def __init__(self, input_color):
        """
        Инициализация цели-1
        points - баллов получено за эту цель
        live
        id -
        id_points - 
        vx - начальная скорость мяча по горизонтали
        vy - начальная скорость мяча по вертикали
        time - параметр для колебаний цели
        is_hitted - проверка, попали в цель или нет(нужна для остановки target.self_coords())
        """
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.vx = rnd(-5, 5)
        self.vy = rnd(-3, 3)
        self.color = input_color
        self.new_target()
        self.time = 0
        self.is_hitted = False

    def new_target(self):
        """ Инициализация новой цели. 
        x - координата по горизонтали. Случайная.
        y - координата по вертикали. Случайная.
        r - радиус. Случайный, но зависит от глобальных start_r, sub_r
        Обновление vx и vy, проверка, что они ненулевые вместе
        """
        global start_r, sub_r
        x = self.x = rnd(600, 1080)
        y = self.y = rnd(200, 500)
        r = self.r = rnd(start_r, 50 - sub_r)
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=self.color)
        while (self.vy == 0) and (self.vx == 0):
            self.vx = rnd(-5, 5)
            self.vy = rnd(-3, 3)
        self.is_hitted = False

    def hit(self, pointss=1):
        """Попадание шарика в цель.
        Флажок is_hitted в True
        Изменение глобальных start_r, sub_r
        Обновление очков за эту цель
        """
        global start_r, sub_r, points, canv_points
        self.is_hitted = True
        canv.coords(self.id, -10, -10, -10, -10)
        points += pointss
        canv.itemconfig(canv_points, text=points)
        start_r -= 3
        if start_r <= 0:
            start_r = 5
        sub_r += 4
        if sub_r >= 44:
            sub_r = 44

    def set_coords(self):
        if not self.is_hitted:
            canv.coords(
                    self.id,
                    self.x - self.r,
                    self.y - self.r,
                    self.x + self.r,
                    self.y + self.r)

    def move(self):
        if self.time == 30:
            self.time = 0
            self.vx = -self.vx
            self.vy = -self.vy
        self.x += self.vx
        self.y -= self.vy
        self.time += 1
        self.set_coords()


t1 = Target('light steel blue')
t2 = Target('indian red')
screen1 = canv.create_text(600, 30, text='', font=("impact", 20))
screen2 = canv.create_text(600, 60, text='', font=("impact", 20))
g1 = Gun()
bullet_1 = 0
bullet_2 = 0
balls = []


def new_game(event=''):
    global t1, t2, screen1, screen2, balls, bullet_1, bullet_2
    t1.new_target()
    t2.new_target()
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    z = 0.03
    t1.live = 1
    t2.live = 1
    while t1.live or balls or t2.live:
        t1.move()
        t2.move()
        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
                if ((bullet_1 % 10) == 1) and (bullet_1 != 11):
                    canv.itemconfig(screen1, text='Вы уничтожили шарик-1 за ' +
                                                  str(bullet_1) + ' выстрел')
                elif ((bullet_1 % 10) <= 4) and ((bullet_1 % 10) >= 2) \
                        and ((bullet_1 <= 12) or (bullet_1 >= 14)):
                    canv.itemconfig(screen1, text='Вы уничтожили шарик-1 за ' +
                                                  str(bullet_1) + ' выстрелa')
                else:
                    canv.itemconfig(screen1, text='Вы уничтожили цель-1 за ' +
                                                  str(bullet_1) + ' выстрелов')

            if b.hittest(t2) and t2.live:
                t2.live = 0
                t2.hit()
                if ((bullet_2 % 10) == 1) and (bullet_2 != 11):
                    canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' +
                                                  str(bullet_2) + ' выстрел')
                elif ((bullet_2 % 10) <= 4) and ((bullet_2 % 10) >= 2) \
                        and ((bullet_2 < 12) or (bullet_2 > 14)):
                    canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' +
                                                  str(bullet_2) + ' выстрелa')
                else:
                    canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' +
                                                  str(bullet_2) + ' выстрелов')

        if t1.live == 0:
            t1.new_target()
            t1.live = 1
        if t2.live == 0:
            t2.new_target()
            t2.live = 1
        canv.update()
        time.sleep(z)
        g1.targetting()
        g1.power_up()

    canv.itemconfig(screen1, text='')
    canv.itemconfig(screen2, text='')
    canv.delete(gun)
    if (t1.live == 0) and (t2.live == 0):
        root.after(100, new_game())


new_game()
mainloop()
