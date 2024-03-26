import zipfile
import optparse
from threading import Thread

def extractFile(zFile, password):
    """
    Attempt to extract a zip file using a given password.
    
    Parameters:
    zFile (ZipFile): The ZipFile object representing the zip file.
    password (str): The password to attempt extraction with.
    """
    try:
        zFile.extractall(pwd=password.encode())
        print('[+] Found Password: ' + password + '\n')
    except Exception as e:
        pass

def main():
    """
    Main function to extract a zip file using a dictionary of passwords.
    """
    # Create an option parser to handle command-line arguments
    parser = optparse.OptionParser("usage%prog "+ "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')

    # Parse the command-line arguments
    (options, args) = parser.parse_args()

    # Check if required arguments are provided
    if options.zname is None or options.dname is None:
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    # Open the zip file
    zFile = zipfile.ZipFile(zname)
    # Open the dictionary file containing passwords
    passFile = open(dname)

    # Iterate through each line in the dictionary file
    for line in passFile.readlines():
        # Strip newline character from the password
        password = line.strip('\n')

        # Create a thread to extract the zip file using the current password
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()

if __name__ == '__main__':
    # If the script is executed directly, run the main function
    main()
