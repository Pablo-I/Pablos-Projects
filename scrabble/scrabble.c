#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{

    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    //Printing the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}


int compute_score(string word)
{
    int charaPoints;
    int currentChar;
    int asciiVal;
    int totalScore = 0;

    //Loops through the entire word to analyze it character by character
    for (int i = 0, L = strlen(word); i < L; i++)
    {
        //Defines the initial character
        currentChar = word[i];

        //Checks lowercase
        if (islower(word[i]))
        {
            //Loop determines what character is being analyzed and how many points to assign to it
            int k = 0;
            do
            {
                asciiVal = k + 97;
                charaPoints = POINTS[k];
                k++;
            }
            while (currentChar != asciiVal);
        }

        //Checks uppercase
        else if (isupper(word[i]))
        {
            //Same as lowercase loop
            int z = 0;
            do
            {
                asciiVal = z + 65;
                charaPoints = POINTS[z];
                z++;
            }
            while (currentChar != asciiVal);
        }
        //Value of 0 is assigned to non-letter characters
        else
        {
            charaPoints = 0;
        }

        totalScore += charaPoints;
    }

    return totalScore;
}
