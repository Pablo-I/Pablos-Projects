#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text;
    int countLetters;
    int countWords;
    int countSentences;

    float L;
    float S;
    float index;

    text = get_string("Text: ");

    countLetters = count_letters(text);
    countWords = count_words(text);
    countSentences = count_sentences(text);

    L = ((float)countLetters / countWords) * 100.0;
    S = ((float)countSentences / countWords) * 100.0;
    index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);

    //Checks what to print based on the index value
    if (index >= 1 && index < 16)
    {
        printf("Grade %i\n", (int)index);
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade 16+\n");
    }
}



int count_letters(string text)
{
    int totalLetters = 0;

    //Loop that evaluates each individual character in the string text
    for (int i = 0, l = strlen(text); i < l; i++)
    {
        //If character is lowercase letter or uppercase, increase counter by 1
        if (islower(text[i]))
        {
            totalLetters += 1;
        }
        else if (isupper(text[i]))
        {
            totalLetters += 1;
        }
        //If character is other, then add 0 to the counter
        else
        {
            totalLetters += 0;
        }

    }

    return totalLetters;
}


int count_words(string text)
{
    int totalWords = 0;

    //Loop that evaluates each individual character in the string text
    for (int i = 0, l = strlen(text); i < l; i++)
    {
        //If a space is encountered, then there was a word before it. Increase word counter by 1
        if (text[i] == ' ')
        {
            totalWords += 1;
        }
    }

    //This final addition to the word counter accounts for the last word (no space after final word)
    totalWords += 1;
    return totalWords;
}


int count_sentences(string text)
{
    int totalSentences = 0;

    //Loop that evaluates each individual character in the string text
    for (int i = 0, l = strlen(text); i < l; i++)
    {
        //If a '.', '!', or '?' is found, then the sentence counter increases by 1
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            totalSentences += 1;
        }
    }

    return totalSentences;
}
