from cs50 import get_string

# Get user input
txt = get_string('Text: ')

# Initialize values. Word starts at one due to counting method.
word = 1
sentence = 0
letter = 0
# Loop through characters int text
for char in txt:
    # If space is found add to word count
    if char == ' ':
        word += 1
    # If period, exclamation, or question mark found, add to sentence
    if char == '.' or char == '!' or char == '?':
        sentence += 1
    # If upper or lowercase letter found, add to letter
    if (ord(char) >= ord('A') and ord(char) <= ord('Z')) or (ord(char) >= ord('a') and ord(char) <= ord('z')):
        letter += 1

# Calculate Coleman-Liau index
L = letter / word * 100
S = sentence / word * 100
CL = 0.0588 * L - 0.296 * S - 15.8

# Round Coleman-Liau index and print grade corresponding to value
if round(CL) < 1:
    print('Before Grade 1')
if round(CL) > 15:
    print('Grade 16+')
else:
    print('Grade ' + str(round(CL)))