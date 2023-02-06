#include <cs50.h>
#include <stdio.h>

// CS50 problem set 1 - Credit
int main(void)
{
    long input = get_long("Number: ");
    // Duplicate input for counting loop
    long num = input;
    // Initialize count
    int count = 0;
    // Count Digits
    while (num != 0)
    {
        num = num / 10;
        count++;
    }
    // Check to ensure correct number digits
    if (count != 13 && count != 15 && count != 16)
    {
        printf("INVALID\n");
        return 0;
    }
    // Initialize variables
    int s1 = 0, s2 = 0, d1, d2, m1, m2;
    long i = input;
    // Perform Checksum
    do
    {
        // Calculate sum of first digits
        d1 = i % 10;
        s1 = s1 + d1;
        // Move to next digit
        i = i / 10;
        // Calculate sum of second digits
        d2 = i % 10;
        d2 = d2 * 2;
        // Manipulate second digits as to sum digits if product > 9
        m1 = d2 % 10;
        m2 = d2 / 10;
        s2 = s2 + m1 + m2;
        // Move to next digit for loop
        i = i / 10;
    }
    while (i != 0);
    int total = s1 + s2;
    // Check Luhn Algorithm
    if (total % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    // If amex card, strip 13 characters and check number
    // Initialize card to declare invalid if all card types fail
    int card = 0;
    int amex = input / 10000000000000;
    if (amex == 34 || amex == 37)
    {
        printf("AMEX\n");
        card = 1;
    }
    // If mastercard, strip 14 characters and check number
    int mc = input / 100000000000000;
    if (mc > 50 && mc < 56)
    {
        printf("MASTERCARD\n");
        card = 1;
    }
    // If visa, strip 12 and 15 characters and check number for each
    int visa1 = input / 1000000000000;
    int visa2 = input / 1000000000000000;
    if (visa1 == 4 || visa2 == 4)
    {
        printf("VISA\n");
        card = 1;
    }
    // State invalid if not matching card found
    if (card == 0)
    {
        printf("INVALID\n");
    }
}