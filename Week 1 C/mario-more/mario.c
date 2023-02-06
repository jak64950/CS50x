#include <cs50.h>
#include <stdio.h>

// CS50 problem set 1 - mario_more
int main(void)
{
    // Declare variables
    int height, space, row, lhash, rhash;
    // Initialize height
    height = 0;
    // Set input bounds
    while (height < 1 || height > 8)
    {
        height = get_int("Height: ");
    }
    // Loop through each row
    for (row = 0; row < height; row++)
    {
        // Loop through left spaces
        for (space = 0; space < height - row - 1; space++)
        {
            printf(" ");
        }
        // Loop through left hashes
        for (lhash = 0; lhash < row + 1; lhash++)
        {
            printf("#");
        }
        // Add gap between pyramids
        printf("  ");
        // Loop through right hashes
        for (rhash = 0; rhash < row + 1; rhash++)
        {
            printf("#");
        }
        // Create new row
        printf("\n");
    }
}