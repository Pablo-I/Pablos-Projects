#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

const int BLOCK_SIZE = 512;

typedef uint8_t BYTE;


int main(int argc, char *argv[])
{
    BYTE buffer[BLOCK_SIZE];
    int counter = -1;
    string filename = malloc(8);

    //Check if one command-line argument is typed
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    //Open the file that contains the images
    FILE *cardSD = fopen(argv[1], "r");
    if (cardSD == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    //Initialize .jpg file (one fo reach jpg)
    FILE *img = fopen("initialize", "w");

    //Loop while a 512 byte block exists
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, cardSD) == BLOCK_SIZE)
    {
        //Check if 512 block includes the header for a jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] >= 0xe0 && buffer[3] <= 0xef))
        {
            //Close current jpg file
            fclose(img);

            //Name and open a new file for the new jpg
            counter++;
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");

            //Write the current 512 byte block to the new jpg file
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);
        }
        else
        {
            //Write the 512 block to the current jpg file
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);
        }
    }

    //Close all files and free malloc() space to prevent leaks
    free(filename);
    fclose(cardSD);
    fclose(img);
    remove("initialize");
}