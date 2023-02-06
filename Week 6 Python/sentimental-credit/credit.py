from cs50 import get_int
import re

# Get card number
cc_int = get_int('Number: ')
# Convert number to string for manipulation
cc = str(cc_int)

# Initialize variables
sum1 = 0
sum2 = 0
# Loop through card number and use Luhn's Algorithm to determine validity
for i in range(len(cc)):
    # Get last digit of card
    y = cc_int % 10
    # Remove last digit of card
    cc_int = cc_int // 10
    # Get original second from last digit of card and multiply by two
    x = 2 * (cc_int % 10)
    # If x is multi-digit add each separately and keep running total
    sum1 += (x % 10) + (x // 10)
    # Keep running total of sums of y
    sum2 += y
    # Remove original second from last digit of card for next iteration
    cc_int = cc_int // 10

# Get total of both sums
sum_tot = sum1 + sum2
# Determine if card is a valid amex, visa, or mastercard
# Test Luhn's Algorithm to see if last digit of total sum is 0
if sum_tot % 10 == 0:
    # Test first digits and length of card to determine card type or print invalid if no match found
    if (re.search('\A34', cc) or re.search('\A37', cc)) and len(cc) == 15:
        print('AMEX')
    elif cc[0] == '5' and int(cc[1]) > 0 and int(cc[1]) < 6 and len(cc) == 16:
        print('MASTERCARD')
    elif cc[0] == '4' and (len(cc) == 13 or len(cc) == 16):
        print('VISA')
    else:
        print('INVALID')
# Invalid if no match found or fails Luhn's Algorithm
else:
    print('INVALID')