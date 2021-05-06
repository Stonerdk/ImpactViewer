from glob import glob
import os
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib.widgets import RadioButtons

def get_impact_time(filename):
    coplist = []
    imapct = -1
    with open(f"{filename}", "r") as f:
        cops, time, tlist, mtime, mratio = [], 0, [], 0, 0
        for line in f.readlines():
            dlist = [int(x) for x in line[21:].split(',')]
            ls = sum(dlist[0:160] + dlist[320:480])
            dlist = dlist[160:320] + dlist[480:640]
            rs = sum(dlist)
            if ls != 0 and rs != 0:
                xs = np.dot(dlist, np.tile(np.arange(16, 32), 20))
                ys = np.dot(dlist, np.repeat(np.arange(19, -1, -1), 16)) + 30 * rs
                cops.append((time, xs / rs, ys / rs))
                sratio = rs / ls
                if sratio > mratio:
                    mtime, mratio = time, sratio
            time += 1
        prev = cops[0]
        for time, xcop, ycop in cops[1:]:
            tprev, xprev, yprev = prev
            tlist.append((time, ((xcop - xprev) ** 2 + (ycop - yprev) ** 2) / (time - tprev)))
            prev = (time, xcop, ycop)
        impact = max(tlist[mtime:], key = lambda x : x[1])[0]
    return cops, impact

class ImpactGraph:
    def __init__(self, filename):
        cops, impact = get_impact_time(filename)

class Viewer:
    def __init__(self, idx):
        global coplist
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.setup(idx)
        # self.canvas = FigureCanvasTkAgg(self.fig, master = root)
        # self.canvas.get_tk_widget().pack(fill='both', expand=True)
        # self.canvas.get_tk_widget().bind('r', lambda event : self.reset())

    def setup(self, idx):
        self.idx = idx
        self.data = coplist[idx]
        self.time, self.x, self.y = list(zip(*self.data))
        self.xy = list(zip(self.x, self.y))
        self.length = len(self.data)
        self.line, = self.ax.plot(self.x, self.y) # simply align xy range
        self.scat = self.ax.scatter(self.x[0], self.y[0])
        self.imp_ans = self.ax.scatter(self.x[impacts[idx]], self.y[impacts[idx]], c = "red", linewidths = 14)
        self.imp_eval = self.ax.scatter(self.x[sol[idx]], self.y[sol[idx]], c = "blue", linewidths = 10) 
        self.pause = False

    def reset(self, idx = -1):
        global coplist
        if idx != -1:
            print(idx)
            self.ax.cla()
            self.setup(idx)
        self.pause = False
        self.anim.frame_seq = self.anim.new_frame_seq()

    def animate(self, i):
        if not self.pause:
            self.line.set_data(self.x[:i + 1], self.y[:i + 1])
            self.scat.set_offsets(self.xy[:i + 1])
            self.imp_eval.set_alpha(1.0 if i >= sol[self.idx] else 0)
            self.imp_ans.set_alpha(1.0 if i >= impacts[self.idx] else 0)
            if i == len(self.x) - 1:
                self.pause = True 
    
    def start(self):
        self.anim = FuncAnimation(self.fig, self.animate, interval = 30)

# initlaize COP lists first
impacts = [59, 67, 86, 81, 50, 51, 61, 61, 65, 57, 61, 58, 56]
flist = glob("./data/*.txt")
coplist, sol = zip(*[get_impact_time(f) for f in flist])
coplist = list(coplist)
sol = list(sol)

for si, s in enumerate(sol):
    print(flist[si], " : evaluated impact time = ", s, "real impact time = ", impacts[si], "error = ", impacts[si] - s)

# initialize TK gui and figure
# root = tk.Tk()
# root.attributes('-fullscreen', True)
# root.title("Impact Viewer")
# lframe = ttk.Frame(root)
# lframe.pack(side = "left")
# rframe = ttk.Frame(root)
# rframe.pack(side = "right")
view = Viewer(0)
# btns = []
mp = {}
for idx, fname in enumerate(flist) :
    mp[fname[13:15]] = idx
rax = plt.axes([0.025, 0.2, 0.075, 0.6])
radio = RadioButtons(rax, tuple(mp.keys()), active=0)
radio.on_clicked(lambda label : view.reset(mp[label]))
#     b.bind("<Button 1>", lambda e, i = idx : view.reset(idx = i))
#     # curious way to bind static
#     b.pack()
#     btns.append(b)
# restart = ttk.Button(lframe, text = "Restart", command = lambda e : view.reset())
# restart.pack()

view.start()
plt.show()