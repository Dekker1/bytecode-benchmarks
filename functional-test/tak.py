#!/usr/bin/env python3

def tak(x, y, z):
    if y < x:
        return tak(tak(x - 1, y, z), tak(y - 1, z, x), tak(z - 1, x, y))
    else:
        return z


if __name__ == "__main__":
    for i in range(1000):
        tak(18, 12, 6)
