def ack(m, n):
	if m == 0:
		return n + 1
	elif n == 0:
		return ack(m-1, 1)
	else:
		return ack(m-1, ack(m,n-1))

if __name__ == "__main__":
    for i in range(1000):
        ack(3, 6)