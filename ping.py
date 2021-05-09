import os
from platform import system
import subprocess
import chardet

def ping(ip_address):
    os_type = system()

    dev_null = open(os.devnull, "w")

    if(os_type == "Windows"):
        try:
            result_bytes = subprocess.check_output(f'ping -n 1 {str(ip_address)}')
            code_dict = chardet.detect(result_bytes)
            result_str = result_bytes.decode(code_dict['encoding']).encode('utf-8')
            result = result_str.decode('utf-8')
            status = result.find('TTL=')
            if status >= 0:
                status = 0
            else:
                status = 1
        except:
            status = 1
    else:
        status = subprocess.call(["ping", "-c", "1", str(ip_address)], stdout=dev_null)
    return status