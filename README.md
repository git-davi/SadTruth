# SadTruth : A simple Open DNS Recursive Resolver list generator
This simple script will output a list of Open DNS Resolver having recursion enabled.  
These servers are likely to be used from hacker or simply disturbed people to do DDOS DNS Amplification attacks.  
- Added multithreading

## Usage  
The simplest use case scenario is to run the script and wait for the list file to be populated with open recursive resolvers.
```bash
$ pip install -r requirements.txt
$ python SadTruth.py
```
This script is also able to make a smarter analysis and output only servers that are more likely to suffer DNS amplification.  
To make the list you only have to run :
```shell
$ python SadTruth.py --amp
```
You can use a custom number of threads.

## Custom initial lists
By default the initial dns list is gathered with OSINT and downloaded from [here](https://public-dns.info/).  
But you can supply your own by simply passing the filename to the command line :
```bash
$ python SadTruth.py --file my_dns_list.txt
```

## Beware Script Kiddies!!
These dns servers can be used for DNS amplification attacks.  
DDOS attacks are illegal so be *wise and responsible* and **use this tool only for threat intel purpose**. 

## Troubleshooting
The script may not work if you are running it over TOR network.