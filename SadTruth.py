import requests
import dns
import dns.message
import dns.query
import dns.flags
import dns.name
import sys
from alive_progress import alive_bar


dns_url = 'https://public-dns.info/nameservers-all.txt'
domain = dns.name.from_text('google.com')


def is_open_recursive(ip):
    # Idenitfy recursive DNS over UDP

    query = dns.message.make_query(domain, dns.rdatatype.A)
    query.flags |= dns.flags.RD
    response = dns.query.udp(query, ip, timeout=2)
    return (response.flags & dns.flags.RA) == dns.flags.RA and len(response.answer) != 0


def append_file(ip):
    with open('dns_list.txt', 'a') as f:
        f.write(ip+'\n')


def main():
    print("[*] Downloading nameserver list")
    r = requests.get(dns_url)
    dns_ips = r.text.split()
    
    print('[*] Wiping previous dns list file')
    open('dns_list.txt', 'w').close()
    print("[*] Found {} dns ips".format(len(dns_ips)))
    print("[*] Begin recursive server discovery phase")
    
    recursive = 0
    progress = 0
    with alive_bar(len(dns_ips)) as bar:
        for ip in dns_ips:
            try:
                if is_open_recursive(ip):
                    append_file(ip)
                    recursive += 1
            except KeyboardInterrupt:
                print('[x] Interrupting')
                print('[*] Found {} open recursive DNS out of {} tested'.format(recursive, progress))
                sys.exit(0)
            except Exception :
                pass
            progress += 1
            bar()


if __name__ == "__main__":
    main()