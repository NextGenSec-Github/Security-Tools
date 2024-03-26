import crypt

def testPass(cryptPass):
    """
    Test a password hash against a dictionary of words.
    
    Parameters:
    cryptPass (str): The password hash to be tested.
    """
    # Extract the salt from the password hash
    salt = cryptPass[0:2]

    # Open the dictionary file
    with open('dictionary.txt', 'r') as dictFile:
        # Iterate through each word in the dictionary
        for word in dictFile.readlines():
            # Strip newline character from the word
            word = word.strip('\n')
            
            # Generate a hash for the current word using the same salt
            cryptWord = crypt.crypt(word, salt)

            # Check if the generated hash matches the provided hash
            if cryptWord == cryptPass:
                # If a match is found, print the password and return
                print("[+] Found Password: " + word + "\n")
                return
    
    # If no match is found after checking all words, print a message
    print("[-] Password Not Found.\n")
    

def main():
    """
    Main function to crack passwords from a file.
    """
    # Open the file containing passwords
    with open('passwords.txt') as passFile:
        # Iterate through each line in the file
        for line in passFile.readlines():
            # Check if the line contains a username and password hash
            if ":" in line:
                # Split the line to extract username and password hash
                user = line.split(':')[0]
                cryptPass = line.split(':')[1].strip(' ')

                # Print message indicating the password cracking process for the current user
                print("[*] Cracking Password For: "+user)

                # Call the function to test the password hash
                testPass(cryptPass)

if __name__ == "__main__":
    # If the script is executed directly, run the main function
    main()

