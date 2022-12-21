# python credit.py
from cs50 import get_int

# Initializing variables
other_Digit = 1
total_X2 = 0
total_XNot = 0
count_Digits = 0
card_Type = "EMPTY"

# Getting credit card number from user
num = get_int("Number: ")

# Loop that checks the validity of the credit card and also checks its type
while num > 0:
    current_Digit = num % 10

    # Check every other digit
    if other_Digit % 2 == 0:
        product = current_Digit * 2
        if product - 10 >= 0:
            for i in range(2):
                total_X2 += product % 10
                product = (product - (product % 10)) / 10
        else:
            total_X2 += product
    # For the digits that were not multiplied
    else:
        total_XNot += current_Digit

    # Check the first two digits of the credit card number to determine credit card type
    if num >= 10 and num <= 99:
        digit_2 = num % 10
        digit_1 = (num - (num % 10)) / 10

        if digit_1 == 3:
            if digit_2 == 4 or digit_2 == 7:
                card_Type = "AMEX"

        elif digit_1 == 5:
            if digit_2 == 1 or digit_2 == 2 or digit_2 == 3 or digit_2 == 4 or digit_2 == 5:
                card_Type = "MASTERCARD"

        elif digit_1 == 4:
            card_Type = "VISA"

    other_Digit += 1
    count_Digits += 1

    # Set-up number to read and assess the new digit
    num -= current_Digit
    num = num / 10

check_Validity = total_X2 + total_XNot

# If no credit card type was determined previously, the the card is invalid regardless of check_Validity
if card_Type == "EMPTY":
    card_Type = "INVALID"

# The following ensures that the number of digits is correct with correspondence to each credit card type
if check_Validity % 10 == 0:
    if card_Type == "AMEX":
        if count_Digits == 15:
            print(f"{card_Type}")
        else:
            print("INVALID")

    elif card_Type == "MASTERCARD":
        if count_Digits == 16:
            print(f"{card_Type}")
        else:
            print("INVALID")

    elif card_Type == "VISA":
        if count_Digits == 13 or count_Digits == 16:
            print(f"{card_Type}")
        else:
            print("INVALID")

    else:
        print("INVALID")

else:
    print("INVALID")
