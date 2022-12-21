#include "helpers.h"
#include "math.h"
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average = 0.0;

    //Loop through the rows (height) and columns (width) of the image[][] array
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            //Check if the colour represented the RGB integers in image[][] are already grey (equal each other)
            if (image[i][k].rgbtBlue != image[i][k].rgbtGreen || image[i][k].rgbtBlue != image[i][k].rgbtRed)
            {
                //Compute the average of the RGB integer values
                average = (image[i][k].rgbtBlue + image[i][k].rgbtGreen + image[i][k].rgbtRed) / 3.0;
                average = round(average);

                //Make the RGB Values equal to produce grey
                image[i][k].rgbtBlue = average;
                image[i][k].rgbtGreen = average;
                image[i][k].rgbtRed = average;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;

    //Loop through the bitmap and reflect the pixels horizontally (along an imaginary vertical line through the middle of the image)
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width / 2; k++)
        {
            temp = image[i][k];
            image[i][k] = image[i][width - k - 1];
            image[i][width - k - 1] = temp;

        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE buffer[height][width];
    float averageBlue = 0.0;
    float averageGreen = 0.0;
    float averageRed = 0.0;


    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            averageBlue = 0.0;
            averageGreen = 0.0;
            averageRed = 0.0;

            //Case 1: left edge
            if (k == 0 && i != 0 && i != height - 1)
            {
                for (int z = -1; z <= 1; z++)
                {
                    for (int j = 0; j < 2; j++)
                    {
                        averageBlue += image[i + z][k + j].rgbtBlue;
                        averageGreen += image[i + z][k + j].rgbtGreen;
                        averageRed += image[i + z][k + j].rgbtRed;
                    }
                }
                averageBlue = round(averageBlue / 6.0);
                averageGreen = round(averageGreen / 6.0);
                averageRed = round(averageRed / 6.0);

                buffer[i][k].rgbtBlue = averageBlue;
                buffer[i][k].rgbtGreen = averageGreen;
                buffer[i][k].rgbtRed = averageRed;
            }


            //Case 2: right edge
            else if (k == width - 1 && i != 0 && i != height - 1)
            {
                for (int z = -1; z <= 1; z++)
                {
                    for (int j = 0; j < 2; j++)
                    {
                        averageBlue += image[i + z][k - j].rgbtBlue;
                        averageGreen += image[i + z][k - j].rgbtGreen;
                        averageRed += image[i + z][k - j].rgbtRed;
                    }
                }
                averageBlue = round(averageBlue / 6.0);
                averageGreen = round(averageGreen / 6.0);
                averageRed = round(averageRed / 6.0);

                buffer[i][k].rgbtBlue = averageBlue;
                buffer[i][k].rgbtGreen = averageGreen;
                buffer[i][k].rgbtRed = averageRed;
            }


            //Case 3: top edge
            else if (i == 0 && k != 0 && k != width - 1)
            {
                for (int z = 0; z < 2; z++)
                {
                    for (int j = -1; j <= 1; j++)
                    {
                        averageBlue += image[i + z][k + j].rgbtBlue;
                        averageGreen += image[i + z][k + j].rgbtGreen;
                        averageRed += image[i + z][k + j].rgbtRed;
                    }
                }
                averageBlue = round(averageBlue / 6.0);
                averageGreen = round(averageGreen / 6.0);
                averageRed = round(averageRed / 6.0);

                buffer[i][k].rgbtBlue = averageBlue;
                buffer[i][k].rgbtGreen = averageGreen;
                buffer[i][k].rgbtRed = averageRed;
            }


            //Case 4: bottom edge
            else if (i == height - 1 && k != 0 && k != width - 1)
            {
                for (int z = 0; z < 2; z++)
                {
                    for (int j = -1; j <= 1; j++)
                    {
                        averageBlue += image[i - z][k + j].rgbtBlue;
                        averageGreen += image[i - z][k + j].rgbtGreen;
                        averageRed += image[i - z][k + j].rgbtRed;
                    }
                }
                averageBlue = round(averageBlue / 6.0);
                averageGreen = round(averageGreen / 6.0);
                averageRed = round(averageRed / 6.0);

                buffer[i][k].rgbtBlue = averageBlue;
                buffer[i][k].rgbtGreen = averageGreen;
                buffer[i][k].rgbtRed = averageRed;
            }


            //Case 5: one of four corners
            else if ((i == 0 && k == 0) || (i == 0 && k == width - 1) || (i == height - 1 && k == 0) || (i == height - 1 && k == width - 1))
            {
                for (int z = 0; z < 2; z++)
                {
                    for (int j = 0; j < 2; j++)
                    {
                        //Top-left corner
                        if (i == 0 && k == 0)
                        {
                            averageBlue += image[i + z][k + j].rgbtBlue;
                            averageGreen += image[i + z][k + j].rgbtGreen;
                            averageRed += image[i + z][k + j].rgbtRed;
                        }

                        //To-right corner
                        if (i == 0 && k == width - 1)
                        {
                            averageBlue += image[i + z][k - j].rgbtBlue;
                            averageGreen += image[i + z][k - j].rgbtGreen;
                            averageRed += image[i + z][k - j].rgbtRed;
                        }

                        //Bottom-left corner
                        if (i == height - 1 && k == 0)
                        {
                            averageBlue += image[i - z][k + j].rgbtBlue;
                            averageGreen += image[i - z][k + j].rgbtGreen;
                            averageRed += image[i - z][k + j].rgbtRed;
                        }

                        //Bottom-right corner
                        if (i == height - 1 && k == width - 1)
                        {
                            averageBlue += image[i - z][k - j].rgbtBlue;
                            averageGreen += image[i - z][k - j].rgbtGreen;
                            averageRed += image[i - z][k - j].rgbtRed;
                        }
                    }
                }
                averageBlue = round(averageBlue / 4.0);
                averageGreen = round(averageGreen / 4.0);
                averageRed = round(averageRed / 4.0);

                buffer[i][k].rgbtBlue = averageBlue;
                buffer[i][k].rgbtGreen = averageGreen;
                buffer[i][k].rgbtRed = averageRed;
            }


            //Case 6: not on edge
            else if (i != 0 && i != height - 1 && k != 0 && k != width - 1)
            {
                for (int z = -1; z <= 1; z++)
                {
                    for (int j = -1; j <= 1; j++)
                    {
                        averageBlue += image[i + z][k + j].rgbtBlue;
                        averageGreen += image[i + z][k + j].rgbtGreen;
                        averageRed += image[i + z][k + j].rgbtRed;
                    }
                }
                averageBlue = round(averageBlue / 9.0);
                averageGreen = round(averageGreen / 9.0);
                averageRed = round(averageRed / 9.0);

                buffer[i][k].rgbtBlue = averageBlue;
                buffer[i][k].rgbtGreen = averageGreen;
                buffer[i][k].rgbtRed = averageRed;
            }
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            image[i][k] = buffer[i][k];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE buffer[height][width];
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    float gxSumBlue = 0;
    float gxSumGreen = 0;
    float gxSumRed = 0;

    float gySumBlue = 0;
    float gySumGreen = 0;
    float gySumRed = 0;

    float gTotalBlue;
    float gTotalGreen;
    float gTotalRed;

    //Loop through each row and column of the bitmap
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            gxSumBlue = 0;
            gxSumGreen = 0;
            gxSumRed = 0;

            gySumBlue = 0;
            gySumGreen = 0;
            gySumRed = 0;

            //Loop through the 3x3 matrix surrounding the current pizel defined by i and k
            for (int z = -1; z <= 1; z++)
            {
                for (int j = -1; j <= 1; j++)
                {
                    //Checks to see if the pixel in the 3x3 matrix is within the bitmap boundaries
                    if ((i + z >= 0 && i + z < height) && (k + j >= 0 && k + j < width))
                    {
                        gxSumBlue += (image[i + z][k + j].rgbtBlue) * gx[z + 1][j + 1];
                        gxSumGreen += (image[i + z][k + j].rgbtGreen) * gx[z + 1][j + 1];
                        gxSumRed += (image[i + z][k + j].rgbtRed) * gx[z + 1][j + 1];

                        gySumBlue += (image[i + z][k + j].rgbtBlue) * gy[z + 1][j + 1];
                        gySumGreen += (image[i + z][k + j].rgbtGreen) * gy[z + 1][j + 1];
                        gySumRed += (image[i + z][k + j].rgbtRed) * gy[z + 1][j + 1];
                    }
                }
            }

            //Compute the total colour values based on gx and gy
            gTotalBlue = round(sqrt(pow(gxSumBlue, 2) + pow(gySumBlue, 2)));
            gTotalGreen = round(sqrt(pow(gxSumGreen, 2) + pow(gySumGreen, 2)));
            gTotalRed = round(sqrt(pow(gxSumRed, 2) + pow(gySumRed, 2)));

            //Ensures that the total is capped at 255
            if (gTotalBlue > 255)
            {
                gTotalBlue = 255;
            }

            if (gTotalGreen > 255)
            {
                gTotalGreen = 255;
            }

            if (gTotalRed > 255)
            {
                gTotalRed = 255;
            }

            buffer[i][k].rgbtBlue = gTotalBlue;
            buffer[i][k].rgbtGreen = gTotalGreen;
            buffer[i][k].rgbtRed = gTotalRed;
        }
    }

    //Populates the image array with the calculated buffer array
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            image[i][k] = buffer[i][k];
        }
    }

    return;
}
