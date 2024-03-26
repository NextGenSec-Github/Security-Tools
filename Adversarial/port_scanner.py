import optparse
from socket import *

def connScan(tgtHost, tgtPort):
    """
    Attempt to establish a TCP connection to the target host and port.

    Parameters:
    tgtHost (str): The target host to scan.
    tgtPort (int): The target port to scan.
    """
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'Adversary\r\n')  # Encode string to bytes
        results = connSkt.recv(100)
        print('[+] %d/tcp open' % tgtPort)
        print('[+] ' + str(results))
        connSkt.close()
    except:
        print('[-] %d/tcp closed' % tgtPort)

def portScan(tgtHost, tgtPorts):
    """
    Perform port scanning on the specified target host and ports.

    Parameters:
    tgtHost (str): The target host to scan.
    tgtPorts (list of int): The target ports to scan.
    """
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan Results for: ' + tgtIP)

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        print('Scanning port ' + str(tgtPort))
        
        try:
            connScan(tgtHost, int(tgtPort))
        except ValueError:
            print("[-] Invalid port number:", tgtPort)

def main():
    """
    Main function to parse command-line arguments and initiate port scanning.
    """
    parser = optparse.OptionParser("usage %prog -H <target host> -p <target port>")
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by commas')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort.split(',') if options.tgtPort else None

    if tgtHost is None or tgtPorts is None:
        print('[-] You must specify a target host and port[s].')
        exit(0)

    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()
