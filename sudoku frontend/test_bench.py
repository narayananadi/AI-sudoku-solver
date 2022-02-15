arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
size = len(arr)
x = 0
while x <= 3:
    temp = arr[0]
    arr.pop(0)
    arr.append(temp)
    x += 1

print(arr)
