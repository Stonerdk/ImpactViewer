from glob import glob
import matplotlib.pyplot as plt 

data_dir = "./data"
file_list = glob(f"{data_dir}/*.txt")
impacts = [59, 67, 86, 81, 50, 51, 61, 61, 65, 57, 61, 58, 56, 64, 59, 52, 64, 45, 50, 51, 47, 69, 65, 90, 83, 68, 108, 56, 58, 53, 55, 55, 55, 59] 
for f_idx, f_name in enumerate(file_list):
    with open(f"{f_name}", "r") as f:
        sensor = []
        xcopl = []
        ycopl = []
        xcopr = []
        ycopr = []
        impactl = None
        impartr = None
        terminall = None
        terminalr = None
        for line in f.readlines():
            data_list = list(map(int, line[21:-1].split(',')))
            sensor.append(data_list)
        for time, dlist in enumerate(sensor):
            xsuml, ysuml, xsumr, ysumr, dsuml, dsumr, p, q = 0, 0, 0, 0, 0, 0, 0, 0
            for i, data in enumerate(dlist):
                if p >= 0 and p < 10:
                    xsuml += (15 - q) * data
                    ysuml += p * data
                    dsuml += data
                elif p >= 10 and p < 20:
                    xsumr += (16 + q) * data
                    ysumr += (19 - p) * data
                    dsumr += data
                elif p >= 20 and p < 30:
                    xsuml += (15 - q) * data
                    ysuml += (p - 10) * data
                    dsuml += data
                elif p >= 30 and p < 40:
                    xsumr += (16 + q) * data
                    ysumr += (49 - p) * data
                    dsumr += data
                q += 1
                if q == 16:
                    p, q = p + 1, 0
            if dsuml != 0:
                Xl, Yl = xsuml / dsuml, ysuml / dsuml
                xcopl.append(Xl)
                ycopl.append(Yl)
                if time == impacts[f_idx]:
                    impactl = (Xl, Yl)
                if time == len(sensor) - 1 :
                    terminall = (Xl, Yl)
            if dsumr != 0:
                Xr, Yr = xsumr / dsumr, ysumr / dsumr
                xcopr.append(Xr)
                ycopr.append(Yr)
                if time == impacts[f_idx]:
                    impactr = (Xr, Yr)
                if time == len(sensor) - 1 :
                    terminalr = (Xr, Yr)
        plt.plot(xcopl, ycopl, "wheat")
        plt.scatter(xcopl, ycopl, c = range(len(xcopl)))
        if impactl:
            plt.scatter([impactl[0]], [impactl[1]], c="red", linewidths = 15)
        if terminall:
            plt.scatter([terminall[0]], [terminall[1]], c="purple", linewidths = 8)

        plt.plot(xcopr, ycopr, "wheat")
        plt.scatter(xcopr, ycopr, c = range(len(xcopr)))
        if impactr:
            plt.scatter([impactr[0]], [impactr[1]], c="red", linewidths = 15)
        if terminalr:
            plt.scatter([terminalr[0]], [terminalr[1]], c="purple", linewidths = 8)
        plt.title(f_name)
        plt.show()