#!/usr/bin/python3

# Created by Mikhail Shchedrin | Conscia Norway
# The script fetches devices from LibreNMS and generates SecureCRT session from an existing one

import jinja2, re, argparse, os, csv
from pprint import pprint

#process cli args
parser = argparse.ArgumentParser()
parser.add_argument("--session-template", help="SecureCRT session(.ini) file to be used as source", required=True)
parser.add_argument("--session-file", help="CSV file for generation sessions", required=True)
args = parser.parse_args()

#open session template file 
sessionTemplate = open(args.session_template,'r').read()
#validate session template file
hostnameRe = re.compile(r'^S:"Hostname"=.*$', flags=re.M)
if not hostnameRe.search(sessionTemplate):
    raise Exception("Invalid session file. It must contain string beginning with '^S:\"Hostname\"='")

# parse csv file to dict
def readCsvFileDict(csvFile):
    with open(csvFile, 'r') as f:
        reader = csv.DictReader(f)
        # for row in reader:
        #     pprint(row)
        return list(reader)

hostList = readCsvFileDict(args.session_file)

for host in hostList:
    hostname = host['hostname']
    ip = host['ip']
    with open(f'sessions/{hostname}.ini', mode='w', newline='\r\n') as sessionFile:
        newSession = hostnameRe.sub(f'S:"Hostname"={ ip }', sessionTemplate)
        sessionFile.write(newSession)
        sessionFile.close()
        print(f"Created {hostname}.ini")
