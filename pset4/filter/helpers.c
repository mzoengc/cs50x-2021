#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int old_blue, old_green, old_red, average;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            old_blue = image[i][j].rgbtBlue;
            old_green = image[i][j].rgbtGreen;
            old_red = image[i][j].rgbtRed;
            // Average on red, green, and blue values
            average = round((old_blue + old_green + old_red) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Create temp array
    RGBTRIPLE image_row_temp[width];
    for (int i = 0; i < height; i++)
    {
        // Copy data to temp array
        for (int j = 0; j < width; j++)
        {
            image_row_temp[j].rgbtBlue = image[i][j].rgbtBlue;
            image_row_temp[j].rgbtGreen = image[i][j].rgbtGreen;
            image_row_temp[j].rgbtRed = image[i][j].rgbtRed;
        }
        // Replace data
        for (int j = 0; j < width; j++)
        {
            int k = width - 1 - j;
            image[i][j].rgbtBlue = image_row_temp[k].rgbtBlue;
            image[i][j].rgbtGreen = image_row_temp[k].rgbtGreen;
            image[i][j].rgbtRed = image_row_temp[k].rgbtRed;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int new_blue, new_green, new_red;
    // Create temp array
    RGBTRIPLE image_temp[height][width];
    // Copy data to temp array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image_temp[i][j].rgbtBlue = image[i][j].rgbtBlue;
            image_temp[i][j].rgbtGreen = image[i][j].rgbtGreen;
            image_temp[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }
    // Calculation
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            int sum_blue = 0;
            int sum_green = 0;
            int sum_red = 0;
            // Find values for 3x3 box
            for (int y = -1; y < 2; y++)
            {
                int height_y = i + y;
                // continue when out of image rows
                if (height_y >= height || height_y < 0)
                {
                    continue;
                }
                // continue when out of image columns
                for (int x = -1; x < 2; x++)
                {
                    int width_x = j + x;
                    if (width_x >= width || width_x < 0)
                    {
                        continue;
                    }
                    // Sum
                    count++;
                    sum_blue += image_temp[height_y][width_x].rgbtBlue;
                    sum_green += image_temp[height_y][width_x].rgbtGreen;
                    sum_red += image_temp[height_y][width_x].rgbtRed;
                }
            }
            // Replace new value - average
            image[i][j].rgbtBlue = round((float)sum_blue / count);
            image[i][j].rgbtGreen = round((float)sum_green / count);
            image[i][j].rgbtRed = round((float)sum_red / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Initial kernels
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    // Create temp array
    RGBTRIPLE image_temp[height][width];
    // Copy data to temp array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image_temp[i][j].rgbtBlue = image[i][j].rgbtBlue;
            image_temp[i][j].rgbtGreen = image[i][j].rgbtGreen;
            image_temp[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }
    // Calculation
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gx_blue = 0;
            int gx_green = 0;
            int gx_red = 0;
            int gy_blue = 0;
            int gy_green = 0;
            int gy_red = 0;
            // Find values for 3x3 box
            for (int y = -1; y < 2; y++)
            {
                int height_y = i + y;
                // continue when out of image rows
                if (height_y >= height || height_y < 0)
                {
                    continue;
                }
                // continue when out of image columns
                for (int x = -1; x < 2; x++)
                {
                    int width_x = j + x;
                    if (width_x >= width || width_x < 0)
                    {
                        continue;
                    }
                    // calculate gx and gy
                    int gx_filter = gx[y + 1][x + 1];
                    int gy_filter = gy[y + 1][x + 1];
                    gx_blue += image_temp[height_y][width_x].rgbtBlue * gx_filter;
                    gx_green += image_temp[height_y][width_x].rgbtGreen * gx_filter;
                    gx_red += image_temp[height_y][width_x].rgbtRed * gx_filter;
                    gy_blue += image_temp[height_y][width_x].rgbtBlue * gy_filter;
                    gy_green += image_temp[height_y][width_x].rgbtGreen * gy_filter;
                    gy_red += image_temp[height_y][width_x].rgbtRed * gy_filter;
                }
            }
            // Do calculation
            image[i][j].rgbtBlue = sobel(gx_blue, gy_blue);
            image[i][j].rgbtGreen = sobel(gx_green, gy_green);
            image[i][j].rgbtRed = sobel(gx_red, gy_red);
        }
    }

    return;
}

int sobel(int gx, int gy)
{
    // √(Gx^2 + Gy^2)
    float result = sqrt((float)gx * gx + gy * gy);
    // check not greater than 255
    if (result > 255)
    {
        return 255;
    }
    return round(result);
}
