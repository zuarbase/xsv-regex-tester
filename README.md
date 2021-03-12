# xsv-regex-tester

```
$ ./regex-tester.py -h
usage: regex-tester [-h] [--encoding ENCODING] [--workdir WORKDIR] [--delimiter DELIMITER] [--json] [--table] [--files] [regex]

regex tester

positional arguments:
  regex                 regular expression (use quotes!)

optional arguments:
  -h, --help            show this help message and exit
  --encoding ENCODING, -e ENCODING
                        optional: include file encoding.
                        defaults to utf-8
  --workdir WORKDIR, -w WORKDIR
                        optional: use a working dir other than the current dir
  --delimiter DELIMITER, -d DELIMITER
                        define a delimiter other than `,`
  --json, -j            print json object
  --table, -t           print table
  --files, -f           only show matching files
```

## Setup (python 3+) 
  
1. clone the git repo
2. cd into the repo folder
3. python -m venv pyenv
4. source pyenv/bin/activate
5. `pip install -r requirements.txt`
  
## Usage  
  
_Show help and exit_   
`$ ./regex-tester.py -h`  
  
_Show matching files using working dir `example-files/`_   
`$ ./regex-tester.py ".+clean.csv" -w example-files -f`  

_Show header names and anything missing using utf-8-sig encoding_   
`$ ./regex-tester.py ".+test-ca.csv" -e utf-8-sig -w example-files`  

_Use a different delimiter_    
`$ ./regex-tester.py ".+clean.csv" -w example-files -d "|"`  
  
_Show a table with header names and positions_  
`$ ./regex-tester.py ".+clean.csv" -w example-files -d "|" -t`  
  
_Output a json object and pipe into jq_  
`$ ./regex-tester.py ".+clean.csv" -w example-files -d "|" -j | jq`  
  
_Use a different delimiter_  
`$ ./regex-tester.py ".+clean.csv" -w example-files -d "|"`  
