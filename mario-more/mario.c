#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("Height (Between 1 and 8): ");
    }
    while (height < 1 || height > 8);

    // For Loop represent each row in the pyramid
    for (int i = 1; i <= height; i++)
    {

        // Two for Loop's used to print the spaces in the inverted pyramid and the following #'s
        for (int k = height; k > i; k--)
        {
            printf(" ");
        }
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }

        printf("  ");

        // For Loop to print out the second pyramid after the two spaces
        for (int z = 1; z <= i; z++)
        {
            printf("#");
        }

        printf("\n");
    }

}