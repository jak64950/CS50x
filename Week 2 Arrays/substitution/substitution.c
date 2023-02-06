#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Simplify expressions
    string x = argv[1];
    // Check user inputs one argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // Check user inputs 26 digit key
    if (strlen(x) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    // Check that all characters are alphabetical and none repeating
    int i = 0;
    while (strlen(x) > i)
    {
        int j = i + 1;
        // Do while loop checks each character in inputted user key for repeating characters
        do
        {
            // Check if values equal regardless if uppercase or lowercase
            if (x[i] == x[j] || x[i] - 32 == x[j] || x[i] + 32 == x[j])
            {
                printf("No repeating characters allowed\n");
                return 1;
            }
            else
            {
                j++;
            }
        }
        while (strlen(x) > j);
        // Check if non alphabetical character
        if (isalpha(x[i]) == 0)
        {
            printf("Key must contain alphabetical characters only.\n");
            return 1;
        }
        i++;
    }
    // Get user plaintext
    string pt = get_string("plaintext: ");
    // Initialize ciphertext by making same as plaintext
    string ct = pt;
    char ex;
    // For loop will convert each character in plaintext to ciphertext equivalent
    for (int k = 0; k < strlen(pt); k++)
    {
        // Map plaintext to ciphertext keeping case
        if (isupper(pt[k]))
        {
            ex = x[pt[k] - 'A'];
            ex = toupper(ex);
        }
        else if (islower(pt[k]))
        {
            ex = x[pt[k] - 'a'];
            ex = tolower(ex);
        }
        // If non alphabetic, don't change
        else
        {
            ex = pt[k];
        }
        // Exchange plaintext for ciphertext
        ct[k] = ex;
    }
    // Print Ciphertext
    printf("ciphertext: %s\n", ct);
    return 0;
}