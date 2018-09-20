# codechef-archive
Json dump of contest/problem data from codechef api.
Helpful for personal experimentation without going over the wire.  
This contains most of the contests/problems till SEPT18 except some for which there was network error.  
For details refer to [extract/codechef_logs.txt](./extract/codechef_logs.txt)

## Usage
```bash
pip3 install -r requirement.txt
cd extract
python3 extract.py | tee codechef_logs.txt
```
