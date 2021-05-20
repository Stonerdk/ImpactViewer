from glob import glob
import os
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib.widgets import RadioButtons

def get_impact_time(filename):
    with open(f"{filename}", "r") as f:
        cops, time, tlist, mtime, midx, mratio = [], 0, [], 0, 0, 0
        idx = 0
        for line in f.readlines():
            dlist = [int(x) for x in line[21:].split(',')]
            ls = sum(dlist[0:160] + dlist[320:480])
            dlist = dlist[160:320] + dlist[480:640]
            rs = sum(dlist)
            if ls != 0 and rs != 0:
                xs = np.dot(dlist, np.tile(np.arange(16, 32), 20))
                ys = np.dot(dlist, np.repeat(np.arange(19, -1, -1), 16)) + 30 * rs
                cops.append([time, xs / rs, ys / rs])
                sratio = rs / ls
                if sratio > mratio:
                    midx, mtime, mratio = idx, time, sratio
                idx += 1
            time += 1
        cops = np.array(cops)
        for i in range(midx + 1, len(cops)):
            dt, dx, dy = cops[i] - cops[i - 1]
            tlist.append([cops[i][0], (dx ** 2 + dy ** 2) / dt])
        tlist = np.array(tlist)
        impact = midx + np.argmax(tlist[:,1]) + 1
    return cops, impact

class Viewer:
    def __init__(self, idx):
        global coplist
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.setup(idx)

    def setup(self, idx):
        self.idx = idx
        self.data = coplist[idx]
        self.time, self.x, self.y = self.data.T
        self.xy = self.data[:, 1:]
        self.length = len(self.data)

        self.line, = self.ax.plot(self.x, self.y) 
        self.scat = self.ax.scatter(self.x[0], self.y[0])
        # self.imp_ans = self.ax.scatter(self.x[impacts[idx]], self.y[impacts[idx]], c = "red", linewidths = 14)
        self.imp_eval = self.ax.scatter(self.x[sol[idx]], self.y[sol[idx]], c = "blue", linewidths = 10) 
        self.pause = False

    def reset(self, idx = -1):
        global coplist
        if idx != -1:
            self.ax.cla()
            self.setup(idx)
        self.pause = False
        self.anim.frame_seq = self.anim.new_frame_seq()

    def animate(self, i):
        if not self.pause:
            self.line.set_data(self.x[:i + 1], self.y[:i + 1])
            self.scat.set_offsets(self.xy[:i + 1])
            self.imp_eval.set_alpha(1.0 if i >= sol[self.idx] else 0)
            # self.imp_ans.set_alpha(1.0 if i >= impacts[self.idx] else 0)
            if i == len(self.x) - 1:
                self.pause = True 
    
    def start(self):
        self.anim = FuncAnimation(self.fig, self.animate, interval = 20)

# initlaize COP lists first
impacts = [59, 67, 86, 81, 50, 51, 61, 61, 65, 57, 61, 58, 56]

flist = glob("./data/*.txt") + glob("./data/saved_util/*.txt") + glob("./data/saved_wood/*.txt")

impacttime = [get_impact_time(f) for f in flist]
coplist, sol = map(list, zip(*impacttime))

for si in range(len(flist)):
    print(flist[si], " : evaluated impact time = ", sol[si])
view = Viewer(0)
mp = {}
for idx, fname in enumerate(flist) :
    mp[fname[6:]] = idx
rax = plt.axes([0.025, 0.2, 0.15, 0.6])
radio = RadioButtons(rax, tuple(mp.keys()), active=0)
radio.on_clicked(lambda label : view.reset(mp[label]))

view.start()
plt.show()