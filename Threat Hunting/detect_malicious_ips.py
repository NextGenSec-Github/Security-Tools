import re
import matplotlib.pyplot as plt

# Define a list of malicious IPs
malicious_ips = []

def load_malicious_ips(file_path):
    """
    Load malicious IP addresses from a file and store them in a set.

    Parameters:
    file_path (str): Path to the file containing malicious IP addresses.

    Returns:
    set: Set of malicious IP addresses.
    """
    with open(file_path, 'r') as file:
        for line in file:
            ip = line.strip()
            malicious_ips.append(ip)
    return set(malicious_ips)

def search_log(file_path, pattern):
    """
    Search a log file for potential threats based on a specified pattern.

    Parameters:
    file_path (str): Path to the log file to be searched.
    pattern (str): Regular expression pattern for extracting IP addresses.

    Returns:
    dict: Dictionary containing counts of malicious IP appearances.
    """
    compiled_pattern = re.compile(pattern)
    malicious_ip_count = {}

    with open(file_path, 'r') as file:
        for line in file:
            ip = compiled_pattern.search(line)
            if ip:
                ip_address = ip.group()
                if ip_address in malicious_ips:
                    if ip_address not in malicious_ip_count:
                        malicious_ip_count[ip_address] = 1
                    else:
                        malicious_ip_count[ip_address] += 1

    return malicious_ip_count

# Example usage:
log_file_path = 'logfile.log'
malicious_ips_file = 'malicious_ips.txt'
search_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# Load malicious IPs
malicious_ips = load_malicious_ips(malicious_ips_file)

# Search log for potential threats and get counts
malicious_ip_counts = search_log(log_file_path, search_pattern)

# Visualization
plt.bar(range(len(malicious_ip_counts)), list(malicious_ip_counts.values()), align='center')
plt.xticks(range(len(malicious_ip_counts)), list(malicious_ip_counts.keys()), rotation=45)
plt.xlabel('Malicious IP Address')
plt.ylabel('Frequency')
plt.title('Occurrences of Malicious IPs in Logs')
plt.tight_layout()
plt.show()

