n = int(input())
current_number = 1
while n > 0:
    print(str(current_number) * min(current_number, n), end='')
    n -= current_number
    current_number += 1
print()
