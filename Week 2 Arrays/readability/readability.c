#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    // Ask user for sentence
    string s = get_string("Text: ");
    float nl = 0, nw = 1, ns = 0, L, S, index;
    // Count letters, words, and sentences
    for (int n = 0; n < strlen(s); n++)
    {
        // Count Letters
        if (isalpha(s[n]) != 0)
        {
            nl++;
        }
        // Count Words
        if (s[n] == ' ')
        {
            nw++;
        }
        // Count Sentences
        if (s[n] == '!' || s[n] == '.' || s[n] == '?')
        {
            ns++;
        }
    }
    // Coleman-Liau index
    L = (nl / nw) * 100;
    S = (ns / nw) * 100;
    index = (0.0588 * L) - (0.296 * S) - 15.8;
    // Round index
    int G = round(index);
    // Customize responses
    if (index < 16 && index >= 1)
    {
        printf("Grade %i\n", G);
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }
}