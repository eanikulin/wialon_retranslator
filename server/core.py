from utils import send_message, get_message, Port
from variables import *
from wialon_parser import parse_message
import threading
import socket
import sys

sys.path.append('../')


class ServerProcessor(threading.Thread):
    """
    Основной класс сервера. Принимает содинения, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    """
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        # Параметры подключения
        self.addr = listen_address
        self.port = listen_port

        # База данных сервера
        self.database = database

        # Сокет, через который будет осуществляться работа
        self.sock = None

        # Флаг продолжения работы
        self.running = True

        # Конструктор предка
        super().__init__()

    def run(self):
        '''Метод основной цикл потока.'''
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while self.running:

            try:
                client, client_address = self.sock.accept()
                message_from_client = get_message(client)
                self.process_client_message(message_from_client)
            except OSError:
                pass
            else:
                print(f'Установлено соедение с ПК {client_address}')
                client.settimeout(5)

    def init_socket(self):
        '''Метод инициализатор сокета.'''
        print(
            f'Запущен сервер, порт для подключений: {self.port} , адрес с которого принимаются подключения: {self.addr}. Если адрес не указан, принимаются соединения с любых адресов.')
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(2)

        # Начинаем слушать сокет.
        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def process_client_message(self, message):
        """ Метод обработчик поступающих сообщений. """
        print('получено сообщение')
        parsed_msg = parse_message(message['test_data'])
        self.database.add_point(message['device_id'], parsed_msg['params'][b'posinfo']['lat'],
                                parsed_msg['params'][b'posinfo']['lon'])
