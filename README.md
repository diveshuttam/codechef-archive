# codechef-archive
Json dump of contest/problem data from codechef api.
Helpful for personal experimentation without going over the wire.  
This contains most of the contests/problems till SEPT18 except some for which there was network error.  
For details refer to [extract/codechef_logs.txt](./extract/codechef_logs.txt)

## Generating archive
```bash
pip3 install -r requirement.txt
cd extract
python3 extract.py | tee codechef_logs.txt
```

## NOTE
The scripts in this repo don't use the actual oauth based api: `https://api.codechef.com/`
instead they use `https://www.codechef.com/api/`.  
The later does not require authentication and doesn't have limits so it becomes easier to archive data. 
The output of the two api endpoints is mostly same, but still there are suttle differenes in keys and data provided.
