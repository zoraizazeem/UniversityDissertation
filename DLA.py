import tkinter as tk
import random
import os
from PIL import ImageGrab
import sys

density = 100
store_dir = "/Users/zoraizazeem/Documents/PProjects/FractalsDiss/clusters/exp2/"
files = os.listdir(store_dir)
iters= []
for file in files:
    if not file.endswith('.DS_Store'):
        num = int(''.join([str(s) for s in file if s.isdigit()]))
        iters.append(num)
iters.sort()

if iters[-1] == 25:
    print("ENDED due to enough iterations done!")
    os._exit(0)

# --- classes ---
r = 5
canv_size = 500

def get_center(a):
    return (((a[0]+a[2])/2), ((a[1]+a[3])/2))

class Ball:

    def __init__(self, x, y, speed_x, speed_y, color):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.shape = canvas.create_oval(x, y, x+(2*r), y+(2*r), fill=color)

    def move(self):

        canvas.move(self.shape, self.speed_x, self.speed_y)

        pos = get_center(canvas.coords(self.shape))

        if pos[1] >= canv_size or pos[1] <= 0:
            self.speed_y = -self.speed_y
        if pos[0] >= canv_size or pos[0] <= 0:
            self.speed_x = -self.speed_x
    def get_posit(self):
        return canvas.coords(self.shape)

    def delete(self):
        canvas.delete(self.shape)

# --- functions ---
def dist(a, b):
    a = get_center(a)
    b = get_center(b)
    return sum([(aItem -bItem)**2 for aItem, bItem in zip(a, b)])



def screenshot():
    
    root.deiconify()
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    x1 = x + root.winfo_width()
    y1 = y + root.winfo_height()
    x_pixels = 337
    y_pixels = 79
    x_screen = 171
    y_screen = 41
    x = x*(x_pixels/x_screen)
    y = y*(y_pixels/y_screen)
    x1 = x1*(x_pixels/x_screen)
    y1 = y1*(y_pixels/y_screen)
    new_file = iters[-1] + 1
    new_file = "{}.png".format(new_file)
    new_file = store_dir +new_file 
    ImageGrab.grab().crop((x, y, x1, y1)).save(new_file)
    print("screenshot taken, file in in: {}".format(new_file))

def move():
    if len(tree) > (0.7*no_free_balls ):
        screenshot()
        print(tree)
        print("Here is the number of balls final: {}".format(len(all_balls)))
        os.execl(sys.executable, sys.executable, *sys.argv)
    for ball in all_balls:
        ball_gone = 0
        posit = ball.get_posit()
        if posit:
            for point_tree in tree:
                distance = dist(posit, point_tree)

                if distance < (r*r*4):
                    canvas.create_oval(posit[0], posit[3], posit[2], posit[1], fill="green")
                    tree.append(posit)
                    ball.delete()
                    ball_gone =1
                    break
            if ball_gone != 1:
                ball.move()

    root.after(100, move)


# --- main ---

root = tk.Tk()
#root.withdraw()
canvas = tk.Canvas(root, width=canv_size, height=canv_size)
canvas.pack()

center = canv_size/2

tree =[(center-r,center-r,center+r,center+r)]
canvas.create_oval(center-r,center-r,center+r,center+r, fill ="yellow")

all_balls = []

for _ in range(density):
    offset_x = random.randint(-4, 4)
    offset_y = random.randint(-4, 4)
    a = random.randint(r, canv_size-r)
    b = random.randint(r, canv_size-r)
    all_balls.append((Ball(a ,b , offset_x, offset_y, "red")))
no_free_balls = len(all_balls)


move()

root.mainloop()
