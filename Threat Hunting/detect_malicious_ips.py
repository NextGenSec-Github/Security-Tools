import bisect
import re

# Define a list of malicious IPs
malicious_ips = []

def load_malicious_ips(file_path):
    """
    Load malicious IP addresses from a file and store them in a sorted list.

    Parameters:
    file_path (str): Path to the file containing malicious IP addresses.

    Returns:
    None
    """
    with open(file_path, 'r') as file:
        for line in file:
            ip = line.strip()
            malicious_ips.append(ip)
    # Sort the list for binary search
    malicious_ips.sort()

def binary_search(arr, target):
    """
    Perform binary search to check if a target exists in a sorted list.

    Parameters:
    arr (list): The sorted list to search.
    target: The value to search for.

    Returns:
    bool: True if the target exists in the list, False otherwise.
    """
    index = bisect.bisect_left(arr, target)
    if index < len(arr) and arr[index] == target:
        return True
    return False

def search_log(file_path, pattern):
    """
    Search a log file for potential threats based on a specified pattern.

    Parameters:
    file_path (str): Path to the log file to be searched.
    pattern (str): Regular expression pattern for extracting IP addresses.

    Returns:
    None
    """
    compiled_pattern = re.compile(pattern)
    with open(file_path, 'r') as file:
        for line in file:
            ip = compiled_pattern.search(line)
            if ip:
                ip_address = ip.group()
                if binary_search(malicious_ips, ip_address):
                    print(f'Potential threat found! IP address {ip_address} found in log')

# Example usage:
log_file_path = 'logfile.log'
malicious_ips_file = 'malicious_ips.txt'
search_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# Load malicious IPs
load_malicious_ips(malicious_ips_file)

# Search log for potential threats
search_log(log_file_path, search_pattern)
