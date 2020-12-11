import requests
import dns
import dns.message
import dns.query
import dns.flags
import dns.name
import sys
from alive_progress import alive_bar
import argparse
import concurrent.futures
import threading


dns_url = 'https://public-dns.info/nameservers-all.txt'
domain = dns.name.from_text('google.com')

parser = argparse.ArgumentParser(description="""
     __           _ _              _   _     
    / _\ __ _  __| | |_ _ __ _   _| |_| |__  
    \ \ / _` |/ _` | __| '__| | | | __| '_ \ 
    _\ \ (_| | (_| | |_| |  | |_| | |_| | | |
    \__/\__,_|\__,_|\__|_|   \__,_|\__|_| |_|
                                         
A simple Open DNS Recursive Resolver list generator.
This script is able to generate a list of DNS server 
vulnerable to recursion and which are likely to be 
used for DDOS DNS amplification attacks.
""", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--file', type=str, help='Your relative filename, for a custom DNS server list')
parser.add_argument('--amp', action='store_true', help='If you want to output only servers more likely to suffer DNS Amplification')
parser.add_argument('-t', dest='threads', type=int, default=5, help='Number of threads')


found = 0
progress = 0
file_lock = threading.Lock()
bar_lock = threading.Lock()


def is_long(resp, threshold=2):
    length = 0
    for rec in resp.answer:
        length += len(rec)
    return length >= threshold


def is_open_recursive(ip, amp):
    # Idenitfy recursive DNS over UDP
    is_recursive = False

    if amp :
        query = dns.message.make_query(domain, dns.rdatatype.ANY)
        query.flags |= dns.flags.RD
        response = dns.query.udp(query, ip, timeout=2)
        is_recursive = (response.flags & dns.flags.RA) == dns.flags.RA and is_long(response)
    else :
        query = dns.message.make_query(domain, dns.rdatatype.TXT)
        query.flags |= dns.flags.RD
        response = dns.query.udp(query, ip, timeout=2)
        is_recursive = (response.flags & dns.flags.RA) == dns.flags.RA and len(response.answer) > 0 
    return is_recursive


def append_file(ip):
    global found

    file_lock.acquire()
    with open('dns_list.txt', 'a') as f:
        f.write(ip+'\n')
        found += 1
    file_lock.release()


def update_bar(bar):
    global progress

    bar_lock.acquire()
    progress += 1
    bar()
    bar_lock.release()


def dns_querier(args):
    ip, amp, bar = args
    try :
        if is_open_recursive(ip, amp):
            append_file(ip)
    except Exception:
        pass
    update_bar(bar)


def main():
    args = parser.parse_args()
    print("[*] Downloading nameserver list")
    r = requests.get(dns_url)
    dns_ips = r.text.split()
    
    print('[*] Wiping previous dns list file')
    open('dns_list.txt', 'w').close()
    print("[*] Found {} dns ips".format(len(dns_ips)))
    print("[*] Begin recursive server discovery phase")
    
    with alive_bar(len(dns_ips)) as bar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            try:
                args_array = [ (ip, args.amp, bar) for ip in dns_ips ]
                futures = executor.map(dns_querier, args_array)
                concurrent.futures.wait(futures)
                print('[*] Found {} open recursive DNS out of {} tested'.format(found, progress))
            except KeyboardInterrupt:
                print('[x] Stopping kindly...')
                executor.shutdown(wait=True)
                print('[*] Found {} open recursive DNS out of {} tested'.format(found, progress))
                sys.exit(0)
            except Exception as e :
                print(e)
            


if __name__ == "__main__":
    main()