# python mario.py
from cs50 import get_int

# Get pyramid height from the user
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

# Iterate through each row of the pyramid
for i in range(1, height+1):

    # First two for loops print out the inverted pyramid
    for k in range(i, height):
        print(" ", end="")

    for j in range(1, i+1):
        print("#", end="")

    # Separte the inverted pyramid and the normal pyramid on the same line
    print("  ", end="")

    # Print out the normal pyramid
    for z in range(1, i+1):
        print("#", end="")

    # Insert new line for next row
    print("")
