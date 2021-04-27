from glob import glob
flist = glob("./data/*.txt")
impacts = [59, 67, 86, 81, 50, 51, 61, 61, 65, 67, 61, 58, 56] 

def get_impact_time(filename):
    with open(f"{filename}", "r") as f:
        cops, time, tlist, prev = [], 0, [], None
        for line in f.readlines():
            dlist = list(map(int, line[21:-1].split(',')))
            dlist = dlist[160:319] + dlist[480:639]
            s = sum(dlist)
            if s == 0:
                continue
            xs, ys, p, q = 0, 30 * s, 19, 16
            for data in dlist:
                xs += q * data
                ys += p * data
                q += 1
                if q == 32:
                    p, q = p - 1, 16
            cops.append((time, xs / s, ys / s))
            time += 1
        for i, (time, xcop, ycop) in enumerate(cops):
            if i != 0:
                tprev, xprev, yprev = prev
                tlist.append((time, ((xcop - xprev) ** 2 + (ycop - yprev) ** 2) / (time - tprev)))
            prev = (time, xcop, ycop)
        impact = max(tlist, key = lambda x : x[1])[0]
        return impact

if __name__ == "__main__" :
    sol = [get_impact_time(f) for f in flist]
    for si, s in enumerate(sol):
        print(flist[si], " : evaluated impact time = ", s, "real impact time = ", impacts[si], "error = ", abs(impacts[si] - s))