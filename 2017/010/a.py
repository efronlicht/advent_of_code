from typing import *

def reverse(a, i, n):
    elem = a[i]
    if i+n > len(a):
        m = (i+n % len(a))
        a = a[m:i] + (a[i:] + a[:m])[::-1]
        print(a)
    else:
        a = (a[:i] + a[i:i+n][::-1] + a[(i+n):])
        print(a)
    return a, a.index(elem)
def main(elems):
    a = list(range(5))
    i, skip = 0, 0
    for n in elems:
        a, i = reverse(a, i, n)
        i = (i+skip) % len(a)
        skip += 1

    return a

print(main([3, 4, 1, 5]))