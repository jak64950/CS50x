#include "helpers.h"
#include "math.h"
#include "stdio.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through rows
    for (int i = 0; i < height; i++)
    {
        // Loop through columns
        for (int j = 0; j < width; j++)
        {
            // Find average of red/green/blue and set each to that average
            float red = image[i][j].rgbtRed, green = image[i][j].rgbtGreen, blue = image[i][j].rgbtBlue;
            int avg = round((red + blue + green) / 3);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through rows
    for (int i = 0; i < height; i++)
    {
        // Loop through columns up to center (to avoid swapping 2x)
        for (int j = 0; j < width / 2; j++)
        {
            // Swap left and right pixels
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create duplicate array from image for average calculations
    RGBTRIPLE dupe[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            dupe[i][j] = image[i][j];
        }
    }
    // Loop through rows
    for (int i = 0; i < height; i++)
    {
        // Loop through columns
        for (int j = 0; j < width; j++)
        {
            // Initialize variables and reset count
            float rsum = 0, gsum = 0, bsum = 0;
            int count = 0;
            // Loop through surrounding pixels
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // Ensure pixel exists
                    if (i - k >= 0 && i - k <= height - 1 && j - l >= 0 && j - l <= width - 1)
                    {
                        // Iteratively add sums using duplicate array
                        rsum += dupe[i - k][j - l].rgbtRed;
                        gsum += dupe[i - k][j - l].rgbtGreen;
                        bsum += dupe[i - k][j - l].rgbtBlue;
                        // Increase count by number of valid surrounding pixels
                        count++;
                    }
                }
            }
            // Update image with calculated sums
            image[i][j].rgbtRed = round(rsum / count);
            image[i][j].rgbtGreen = round(gsum / count);
            image[i][j].rgbtBlue = round(bsum / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create duplicate array of image for calculations
    RGBTRIPLE dupe[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            dupe[i][j] = image[i][j];
        }
    }
    // Initialize Gx and Gy kernels from Sobel operator
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    // Loop through rows
    for (int i = 0; i < height; i++)
    {
        // Loop through columns
        for (int j = 0; j < width; j++)
        {
            // Initialize variables
            float GxR = 0, GxG = 0, GxB = 0, GyR = 0, GyG = 0, GyB = 0;
            // Loop through surrounding pixels
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // Ignore pixels which don't exist from calculation
                    if (i - k >= 0 && i - k <= height - 1 && j - l >= 0 && j - l <= width - 1)
                    {
                        // Iteratively add sums using duplicate array
                        GxR += dupe[i - k][j - l].rgbtRed * Gx[1 - k][1 - l];
                        GxG += dupe[i - k][j - l].rgbtGreen * Gx[1 - k][1 - l];
                        GxB += dupe[i - k][j - l].rgbtBlue * Gx[1 - k][1 - l];
                        GyR += dupe[i - k][j - l].rgbtRed * Gy[1 - k][1 - l];
                        GyG += dupe[i - k][j - l].rgbtGreen * Gy[1 - k][1 - l];
                        GyB += dupe[i - k][j - l].rgbtBlue * Gy[1 - k][1 - l];
                    }
                }
            }
            // Perform Sobel calculation, rounding to the nearest integer
            int red = round(sqrt(GxR * GxR + GyR * GyR));
            int green = round(sqrt(GxG * GxG + GyG * GyG));
            int blue = round(sqrt(GxB * GxB + GyB * GyB));
            // Cap value at 255
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }
            // Update image with new values
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}
