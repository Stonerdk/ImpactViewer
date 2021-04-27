from glob import glob

def get_impact_time(filename):
    imapct = -1
    with open(f"{filename}", "r") as f:
        cops, time, tlist, mtime, mratio = [], 0, [], 0, 0
        for line in f.readlines():
            dlist = list(map(int, line[21:-1].split(',')))
            ls = sum(dlist[0:159] + dlist[320:479])
            dlist = dlist[160:319] + dlist[480:639]
            rs = sum(dlist)
            if ls != 0 and rs != 0:
                sratio = rs / ls
                xs, ys, p, q = 0, 30 * rs, 19, 16
                for data in dlist:
                    xs += q * data
                    ys += p * data
                    q += 1
                    if q == 32:
                        p, q = p - 1, 16
                cops.append((time, xs / rs, ys / rs))
                if sratio > mratio:
                    mtime, mratio = time, sratio
            time += 1
        prev = cops[0]
        for time, xcop, ycop in cops[1:]:
            # print(time, xcop, ycop)
            tprev, xprev, yprev = prev
            tlist.append((time, ((xcop - xprev) ** 2 + (ycop - yprev) ** 2) / (time - tprev)))
            prev = (time, xcop, ycop)
        # print(cops)
        # print(tlist[mtime:])
        impact = max(tlist[mtime:], key = lambda x : x[1])[0]
    return impact

if __name__ == "__main__" :
    flist = glob("./data/*.txt")

    impacts = [59, 67, 86, 81, 50, 51, 61, 61, 65, 57, 61, 58, 56] 
    sol = [get_impact_time(f) for f in flist]
    for si, s in enumerate(sol):
        print(flist[si], " : evaluated impact time = ", s, "real impact time = ", impacts[si], "error = ", abs(impacts[si] - s))