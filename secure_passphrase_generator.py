from bs4 import BeautifulSoup
import requests
import random
import re

# Passphrase generation settings
word_count = 5
word_min_len = 10
word_max_len = 15
num_len = 3
num_per_word = 2

print("\nSecure Passphrase Generator - Daniel Kasprzyk")
print("       Made thanks to untroubled.org"         )
print("---------------------------------------------\n")

print("Settings:")
print("---------")
word_count = int(input("Number of words to include? "))
word_min_len = int(input("Minimum word length? "))
word_max_len = int(input("Maximum word length? "))
num_len = int(input("Length of numbers between words? "))
num_per_word = int(input("Letter/number substitutions per word? "))
print()

# Used for mapping characters
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
num_mapping = ['4', '6', '7', '6', '3', '4', '9', '6', '1', '1', '7', '1', '3', '5', '0', '9', '9', '2', '5', '7', '8', '8', '9', '9', '9', '2']
special_characters = ['_', '-', '!', '?', '@', '#', '£', '$', '%', '^', '&', '*', '(', ')', '=', '+', '<', '>']

# Obtain passphrases from the webpage with current config
url = f'https://untroubled.org/pwgen/ppgen.cgi?wordcount={word_count}&minlen={word_min_len}&maxlen={word_max_len}&randcaps=first&numlen={num_len}&submit=Generate+Passphrase'
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables
    tables = soup.find_all('table')
    
    # Extract passphrases from its table
    last_table = tables[-1]
    tds = last_table.find_all('td')
    passphrases = [td.get_text(strip=True).replace("'", "") for td in tds]

    for index in range(len(passphrases)):
        # Break passphrase apart into words and numbers
        deconstructed_passphrase = re.split(r'(\d+)', passphrases[index])

        # Remove empty elements from the split result
        deconstructed_passphrase = [element for element in deconstructed_passphrase if element]

        for i in range(len(deconstructed_passphrase)):
            item = deconstructed_passphrase[i]

            # Adding special characters to passphrase - number part
            try:
                int(item) # Temp cast to determine whether item is an int
                str(item)
                position = random.randint(0, 1)
                special_char = special_characters[random.randint(0, len(special_characters) - 1)]
                if position == 0:
                    deconstructed_passphrase[i] = f"{special_char}{item}"
                elif position == 1:
                    deconstructed_passphrase[i] = f"{item}{special_char}"

            # Substituting letters with number equivalents - word part
            except ValueError:
                temp_passphrase = list(item)

                # Get a list of random indices to change
                indices_to_change = random.sample(range(1, len(temp_passphrase)), num_per_word)

                # Substitute the letters at the random indices
                for j in indices_to_change:
                    if temp_passphrase[j] in alphabet:
                        letter_index = alphabet.index(temp_passphrase[j])
                        temp_passphrase[j] = num_mapping[letter_index]

                # Convert the list back to a string
                new_passphrase = ''.join(temp_passphrase)
                deconstructed_passphrase[i] = new_passphrase

        # Update the current passphrase
        passphrases[index] = ''.join(deconstructed_passphrase)

    print("Passphrases:")
    for passphrase in passphrases:
        print(passphrase)

else:
    print('Error - Failed to fetch the webpage.')


