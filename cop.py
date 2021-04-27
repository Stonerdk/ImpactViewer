from glob import glob
import matplotlib.pyplot as plt 

data_dir = "./data_apgujung"
file_list = glob(f"{data_dir}/*.txt")
impacts = [59, 67, 86, 81, 50, 51, 61, 61, 65, 57, 61, 58, 56, 64, 59, 52, 64, 45, 50, 51, 47, 69, 65, 90, 83, 68, 108, 56, 58, 53, 55, 55, 55, 59] 
for f_idx, f_name in enumerate(file_list):
    with open(f"{f_name}", "r") as f:
        sensor = []
        xcop = []
        ycop = []
        impact = None
        terminal = None
        for line in f.readlines():
            data_list = list(map(int, line[21:-1].split(',')))
            sensor.append(data_list)
        for time, dlist in enumerate(sensor):
            xsum, ysum, dsum, p, q = 0, 0, 0, 0, 0
            for i, data in enumerate(dlist):
                if p >= 0 and p < 10:
                    xsum += (15 - q) * data
                    ysum += p * data
                elif p >= 10 and p < 20:
                    xsum += (16 + q) * data
                    ysum += (19 - p) * data
                elif p >= 20 and p < 30:
                    xsum += (15 - q) * data
                    ysum += (p - 10) * data
                elif p >= 30 and p < 40:
                    xsum += (16 + q) * data
                    ysum += (49 - p) * data
                q += 1
                dsum += data
                if q == 16:
                    p, q = p + 1, 0
            X, Y = xsum / dsum, ysum / dsum
            xcop.append(X)
            ycop.append(Y)
            if time == impacts[f_idx]:
                impact = (X, Y)
            if time == len(sensor) - 1 :
                terminal = (X, Y)
        plt.plot(xcop, ycop, "wheat")
        plt.scatter(xcop, ycop, c = range(len(sensor)))
        plt.scatter([impact[0]], [impact[1]], c="red", linewidths = 15)
        plt.scatter([terminal[0]], [terminal[1]], c="purple", linewidths = 8)
        plt.show()