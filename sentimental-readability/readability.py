# python readability.py
from cs50 import get_string


def main():
    # Get String from user
    text = get_string("Text: ")

    # Count the number of letters, words, and sentences
    countLetters = count_letters(text)
    countWords = count_words(text)
    countSentences = count_sentences(text)

    # Compute the Coleman-Liau index
    L = (countLetters / countWords) * 100.0
    S = (countSentences / countWords) * 100.0
    index = 0.0588 * L - 0.296 * S - 15.8
    index = round(index, 0)

    # Print the Grade (ie. index) accordingly
    if index >= 1 and index < 16:
        print(f"Grade {index}")
    elif index < 1:
        print("Before Grade 1")
    else:
        print("Grade 16+")


# Count the number of letters in the text
def count_letters(text):
    totalLetters = 0

    for i in range(0, len(text)):
        # Check if the current character is a lower case letter
        if ord(text[i]) >= 97 and ord(text[i]) <= 122:
            totalLetters += 1
        # Check if the current character is an upper case letter
        elif ord(text[i]) >= 65 and ord(text[i]) <= 90:
            totalLetters += 1
        # Check if the current character is anything but a letter
        else:
            totalLetters += 0

    return totalLetters


# Counts the number of words in the text
def count_words(text):
    totalWords = 0

    for k in range(0, len(text)):
        # Count the number of spaces (a space comes after each word)
        if text[k] == " ":
            totalWords += 1

    # Account for the last word (there is no space after the last word)
    totalWords += 1
    return totalWords


# Counts the number of senteces in the text
def count_sentences(text):
    totalSentences = 0

    for z in range(0, len(text)):
        # Assume that a ., ?, or ! indicates the end of a sentence
        if text[z] == '.' or text[z] == '!' or text[z] == '?':
            totalSentences += 1

    return totalSentences


main()
