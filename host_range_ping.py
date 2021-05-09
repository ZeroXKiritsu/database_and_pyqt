import ipaddress
import socket
import ping

def host_range_ping(is_loop_ip):
    success_request = "Узел доступен"
    fail_request = "Узел недоступен"
    fail_ip_address = "Имя узла задано некорректно"

    columns = ['адрес', 'результат']
    result = []

    print(f"Сканер запущен... Поиск по диапазону {is_loop_ip[0]} : {is_loop_ip[len(is_loop_ip) - 1]}")

    i = 0
    for ip in is_loop_ip:
        request_dict = dict()
        try:
            ip_address = ipaddress.ip_address(ip)
            status = ping.ping(ip_address)
            if status == 0:
                request_dict[columns[0]] = str(ip_address)
                request_dict[columns[1]] = success_request
            else:
                request_dict[columns[0]] = str(ip_address)
                request_dict[columns[1]] = fail_request
        except:
            try:
                ip_address = socket.gethostbyname(ip)
                status = ping.ping(ip_address)
                if status == 0:
                    request_dict[columns[0]] = str(ip)
                    request_dict[columns[1]] = success_request
                else:
                    request_dict[columns[0]] = str(ip)
                    request_dict[columns[1]] = fail_request
            except:
                request_dict[columns[0]] = str(ip)  # внесем ip, хоть это и не является адресом
                request_dict[columns[1]] = fail_ip_address
        result.append(request_dict)
        print(f"{result[i][columns[0]]} | {result[i][columns[1]]}")
        i += 1
    return result

if __name__ == '__main__':
    ip_1 = '192.168.2.1'
    ip_2 = '192.168.1.253'

    ip_1 = ipaddress.IPv4Address(ip_1)
    ip_2 = ipaddress.IPv4Address(ip_2)

    loop_ip = []

    if ip_1 > ip_2:
        ip_2, ip_1 = ip_1, ip_2

    v_ip = ip_1

    while v_ip <= ip_2:
        loop_ip.append(str(v_ip))
        v_ip = v_ip + 1

    host_range_ping(loop_ip)