#include <cs50.h>
#include <stdio.h>
#include<string.h>

int main(void)
{
    //Initializing and declaring variables
    long num;
    int other_Digit = 1;
    int current_Digit;
    int product;
    int digit_1;
    int digit_2;
    int count_Digits = 0;

    int total_X2 = 0;
    int total_XNot = 0;
    string card_Type = "EMPTY";
    int check_Validity;


    //Get credit card number 4003600000000014
    num = get_long("Number: ");

    //While loop that checks the validity/credit card type
    while (num > 0)
    {
        current_Digit = num % 10;

        //Check to see if the digit is the "other digit"
        if (other_Digit % 2 == 0)
        {
            product = current_Digit * 2;

            if (product - 10 >= 0)
            {
                for (int i = 0; i < 2; i++)
                {
                    total_X2 += product % 10;
                    product = (product - (product % 10)) / 10;
                }
            }
            else
            {
                total_X2 += product;
            }
        }

        //Check to see if this corresponds to the digits that were not multiplied by 2
        else
        {
            total_XNot += current_Digit;
        }

        //Checks the first two digits of the credit card number to determine credit card type
        if (num >= 10 && num <= 99)
        {
            digit_2 = num % 10;
            digit_1 = (num - (num % 10)) / 10;

            if (digit_1 == 3)
            {
                if (digit_2 == 4 || digit_2 == 7)
                {
                    card_Type = "AMEX";
                }
            }
            else if (digit_1 == 5)
            {
                if (digit_2 == 1 || digit_2 == 2 || digit_2 == 3 || digit_2 == 4 || digit_2 == 5)
                {
                    card_Type = "MASTERCARD";
                }
            }
            else if (digit_1 == 4)
            {
                card_Type = "VISA";
            }
        }

        other_Digit += 1;
        count_Digits += 1;

        //Set-up number to read and assess the new digit
        num -= current_Digit;
        num = num / 10;
    }

    check_Validity = total_X2 + total_XNot;

    //If no credit card type was determined previously, the the card is invalid regardless of check_Validity
    if (strcmp(card_Type, "EMPTY") == 0)
    {
        card_Type = "INVALID";
    }

    //The following ensures that the number of digits is correct with correspondence to each credit card type
    if (check_Validity % 10 == 0)
    {
        if (strcmp(card_Type, "AMEX") == 0)
        {
            if (count_Digits == 15)
            {
                printf("%s\n", card_Type);
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (strcmp(card_Type, "MASTERCARD") == 0)
        {
            if (count_Digits == 16)
            {
                printf("%s\n", card_Type);
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (strcmp(card_Type, "VISA") == 0)
        {
            if (count_Digits == 13 || count_Digits == 16)
            {
                printf("%s\n", card_Type);
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}