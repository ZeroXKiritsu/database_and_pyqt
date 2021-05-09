import ipaddress
import socket
import ping

def host_ping(is_loop_ip):
    success_request = "Узел доступен"
    fail_request = "Узел недоступен"
    fail_ip_address = "Имя узла задано некорректно"

    columns = ['адрес', 'результат']
    result = []

    print("Сканер запущен...")

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
                request_dict[columns[0]] = str(ip)
                request_dict[columns[1]] = fail_ip_address
        result.append(request_dict)
        print(f"{result[i][columns[0]]} | {result[i][columns[1]]}")
        i += 1
    return result

if __name__ == '__main__':
    loop_ip = ['192.168.1.1', '192.168.1.2', '127.0.0.1', '192.168.0.1', '192.168.1.126', '127', 'ya.ru']
    host_ping(loop_ip)