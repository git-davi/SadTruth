# SadTruth : A simple Open DNS Recursive Resolver list generator
This simple script will output a list of Open DNS Resolver having recursion enabled.  
It may take time...

## Usage  
The simplest use case scenario is to run the script and wait for the list file to be populated with open recursive resolvers.
```bash
$ pip install -r requirements.txt
$ python SadTruth.py
```

## Custom initial lists
By default the initial dns list is gathered with OSINT and downloaded from `https://public-dns.info/`.  
But you can use your own by simply replacing the get response content with a `f.read()` or the `url` with your own.  

## Beware Script Kiddies!!
These dns servers can be used for DNS amplification attacks.  
DOS is an illegal so be *wise and responsible* and **use this tool only for threat intel purpose**. 