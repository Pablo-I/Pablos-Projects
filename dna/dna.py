# python dna.py databases/small.csv sequences/1.txt
import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    # Initialize empty list for the dna data base
    database = []

    # Open the file for reading (with open() closes the file automatically once it's done reading from it)
    with open(sys.argv[1]) as dnaDatabase:
        reader = csv.DictReader(dnaDatabase)
        # Each name represents a dictionary which is then stored in the data base list (each element in the data base list is a dictionary)
        for name in reader:
            database.append(name)

        # Convert the STR's to integers (they are read as strings)
        for name in database:
            for key in name:
                if key != "name":
                    name[key] = int(name[key])

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as dnaSequence:
        sequence = dnaSequence.readline().strip()

    # TODO: Find longest match of each STR in DNA sequence
    # define a dictionary that will store the longest match of each STR in the dna sequence (the key is the STR itself)
    strMatches = {}

    # For each STR, store the longest match found in the dna sequence, along with the STR as the key, in strMatches{}
    for key in database[0]:
        if key != "name":
            strMatches[key] = longest_match(sequence, key)

    # TODO: Check database for matching profiles
    # Define dictionary that will store the STR's and their corresponding longest match integer.
    check = {}
    for name in database:
        # Make check equal to the current name being assessed
        check = name
        tempName = check["name"]
        del check["name"]
        # If strMatches{} equals the check{} dictionary of the current person, then this is their dna
        if strMatches == check:
            print(tempName)
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
