#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check if entered proper inputs
    if (argc != 2)
    {
        printf("Usage: recover [file]\n");
        return 1;
    }
    // Check file is readable
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Error: Could not open %s.\n", argv[1]);
        return 1;
    }
    // Simplify uint8_t to BYTE
    typedef uint8_t BYTE;
    // Intiliaze variables for upcoming loop
    int size = 512, i = 0;
    // Set buffer to block size for reading/writing data from memory card
    BYTE buffer[size];
    // Initialize file will be writing to from buffer
    FILE *img = NULL;
    // Initialize array for filename
    char jpg[8];
    // Loop through all of memory card data. When data left is less than block size, then abort
    while (fread(buffer, 1, size, file) == size)
    {
        // Check beginning block for known jpeg data
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous image writing to
            if (i != 0)
            {
                fclose(img);
            }
            // Create new jpeg and open it for writing
            sprintf(jpg, "%03i.jpg", i);
            img = fopen(jpg, "w");
            // Increment jpeg number
            i++;
        }
        // Write to opened jpeg file
        if (i != 0)
        {
            fwrite(buffer, 1, size, img);
        }
    }
    // Close any open files
    fclose(file);
    fclose(img);
    return 0;
}