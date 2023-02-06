import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print('Correct Usage: dna.py csv txt')
        return 1

    # Read database file into a variable
    csvfile = open(sys.argv[1])
    db = csv.reader(csvfile)

    # Read DNA sequence file into a variable
    txtfile = open(sys.argv[2])
    txt = txtfile.read()

    # Find longest match of each STR in DNA sequence
    # Get first row of db
    row1 = next(db)
    longest = []
    # Feed sequence and subsequence into longest_match function
    for i in range(1, len(row1)):
        longest.append(longest_match(txt, row1[i]))

    # Check database for matching profiles
    for i in db:
        # Remove name of list
        name = i.pop(0)
        # Convert list strings to integers
        i = [int(x) for x in i]
        # Print name if DNA match found and close files
        if i == longest:
            print(name)
            csvfile.close
            txtfile.close
            return 0
    # Print no match if no match found and close files
    print('No match')
    csvfile.close
    txtfile.close

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
