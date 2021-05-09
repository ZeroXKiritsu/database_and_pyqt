import ipaddress
from tabulate import tabulate
import host_range_ping

def host_range_ping_tab():
    ip_1 = '192.168.1.1'
    ip_2 = '192.168.1.10'

    ip_1 = ipaddress.IPv4Address(ip_1)
    ip_2 = ipaddress.IPv4Address(ip_2)

    loop_ip = []

    if ip_1 > ip_2:
        ip_2, ip_1 = ip_1, ip_2

    v_ip = ip_1
    while v_ip <= ip_2:
        loop_ip.append(str(v_ip))
        v_ip = v_ip + 1

    table_result = host_range_ping.host_range_ping(loop_ip)
    print(tabulate(table_result, headers='keys', tablefmt="orgtbl"))

if __name__ == '__main__':
    host_range_ping_tab()
