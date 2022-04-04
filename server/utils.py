"""Утилиты"""

import json
import sys

sys.path.append('../')
from variables import *


# Утилита приёма и декодирования сообщения
# принимает байты выдаёт словарь, если принято что-то другое отдаёт ошибку типа
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


# Утилита кодирования и отправки сообщения
# принимает словарь и отправляет его
def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)


class Port:
    """
    Позволяет использовать только порты с 1023 по 65536.
    При попытке установить неподходящий номер порта генерирует исключение.
    """

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            print(
                f"Попытка запуска с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535."
            )
            raise TypeError("Некорректрый номер порта")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
