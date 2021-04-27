dlist = [1 for _ in range(640)]
p, q, xsum, ysum, dsum = 0, 0, 0, 0, 0
xcop, ycop = [], []
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
print(xsum, ysum, dsum)
xcop.append(xsum / dsum)
ycop.append(ysum / dsum)
print(xcop)
print(ycop)