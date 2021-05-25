import logging

SERVER_LOGGER = logging.getLogger('server')

class PortValidate:
    def __set__(self, instance, value):
        try:
            ip_port = int(value)
            if ip_port < 1025 or ip_port > 65535:
                SERVER_LOGGER.critical(f"Порт должен быть от 1024 до 65535. Попытка старта с портом {value}")
                exit(1)
            else:
                instance.__dict__[self.name] = value
        except:
            SERVER_LOGGER.critical(f"Порт должен быть целым числом от 1024 до 65535. Попытка старта с портом {value}")
            exit(1)

    def __set_name__(self, owner, name):
        self.name = name


class IPValidate:
    def __set__(self, instance, value):
        tmp_str = value.split('.')
        if len(tmp_str) != 4:
            SERVER_LOGGER.critical(f"Некорректно указан IP адрес: {value} ")
            exit(1)
        for el in tmp_str:
            if not el.isdigit():
                SERVER_LOGGER.critical(f"Некорректно указан IP адрес: {value}")
                exit(1)
            i = int(el)
            if i < 0 or i > 255:
                SERVER_LOGGER.critical(f"Некорректно указан IP адрес: {value}")
                exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name