#!/usr/bin/env python3


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    for i in range(1000):
        fib(23)
