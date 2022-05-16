#!/usr/bin/python3

import argparse, re, sys, subprocess
from tabulate import tabulate as tb

arguments = argparse.ArgumentParser()
arguments.add_argument("-n", "--host", required=True, help="IP Address for scanning")

arg = arguments.parse_args()

def GetTTL():

    try:
        ping_process = subprocess.Popen(["/usr/bin/ping -c 1 %s " %(arg.host)], stdout=subprocess.PIPE, shell=True)
        output, error = ping_process.communicate()
        output = output.split()
        output = output[12].decode('utf-8')
        ttl = re.findall(r"\d{1,3}", output)[0]
    
        return ttl
    except IndexError:
        print("Index Error: Lista fuera de rango\n")
        return 1
        

def GetOsName(ttl):

    ttl = int(ttl)

    if ttl >= 2 and ttl <= 64:
        return "Unix/Linux"
    elif ttl >= 64 + 1 and ttl <= 128:
        return "Windows"
    elif ttl == 1:
        return "Unknown"
    elif ttl == 255:
        return "Solaris"
    else:
        return "Not Found"


if __name__ == "__main__":
    print()
    call_ttl = GetTTL()
    whichOS = GetOsName(call_ttl)
    print(tb([[f'{arg.host}', f'{call_ttl}', f'{whichOS}']], headers=['IP', 'TTL', 'OS'], tablefmt='pretty'))
