from cs50 import get_int

# Get height of pyramid from user
n = get_int('Height: ')
# Pyramid height must be between 1 and 8 inclusive
while n not in range(1, 9):
    n = get_int('Height: ')
# Print pyramid based on height
for i in range(n):
    print(' ' * (n-i-1), '#' * (i+1), '  ', '#' * (i+1), sep='')