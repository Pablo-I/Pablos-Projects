#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int check_cipher(int argC, string argV[]);
int cipher_text(string text, string code);

int main(int argc, string argv[])
{
    int exitCheck;
    string plaintext;
    string code;

    //Checks if the code is valid. If not, the program exits.
    exitCheck = check_cipher(argc, argv);
    if (exitCheck == 1)
    {
        return 1;
    }

    code = argv[1];
    plaintext = get_string("plaintext: ");

    //Converts the users text to the corresponding encrypted code. returns 0 to show the task was successful.
    exitCheck = cipher_text(plaintext, code);

    return exitCheck;
}



int check_cipher(int argC, string argV[])
{
    string cipherCode;
    int cipherSize;
    int currentChar;

    //Checks to see if a single cipher code has been correctly typed in.
    if (argC != 2)
    {
        printf("Usage: substitution key\n");
        return 1;
    }

    cipherCode = argV[1];
    cipherSize = strlen(cipherCode);

    //Checks that the total number of characters in code is 26.
    if (cipherSize != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    //Checks all characters to ensure they are valid.
    for (int i = 0; i < cipherSize; i++)
    {
        currentChar = cipherCode[i];
        if (islower(currentChar) == 0 && isupper(currentChar) == 0)
        {
            printf("Cipher code can only include alphabetical characters.\n");
            return 1;
        }
    }

    //Loop that checks for duplicate characters.
    for (int k = 0; k < cipherSize; k++)
    {
        for (int i = 0; i < cipherSize; i++)
        {
            if (cipherCode[k] == cipherCode[i] && i != k)
            {
                printf("Alphabetical characters cannot repeat in the cipher code.\n");
                return 1;
            }
        }
    }

    return 0;
}


int cipher_text(string text, string code)
{
    int currentChar;
    int textSize;
    int cipherSize;
    int charPos;
    string codedText = text;

    textSize = strlen(text);
    cipherSize = strlen(code);

    //First for loop analyzes the users text character by character.
    for (int i = 0; i < textSize; i++)
    {
        currentChar = text[i];

        //Second for loop compares the current text character being analyzed to the entire code key.
        for (int z = 0; z < cipherSize; z++)
        {
            //Checks if the current character is upper or lower case and determines its corresponding code character accordingly.
            if (islower(currentChar))
            {
                charPos = currentChar - 97;
                if (charPos == z)
                {
                    if (islower(code[z]))
                    {
                        codedText[i] = code[z];
                    }
                    else
                    {
                        codedText[i] = code[z] + 32;
                    }
                }
            }
            else if (isupper(currentChar))
            {
                charPos = currentChar - 65;
                if (charPos == z)
                {
                    if (isupper(code[z]))
                    {
                        codedText[i] = code[z];
                    }
                    else
                    {
                        codedText[i] = code[z] - 32;
                    }
                }
            }
            else
            {
                codedText[i] = text[i];
            }
        }
    }

    printf("ciphertext: %s\n", codedText);

    return 0;
}