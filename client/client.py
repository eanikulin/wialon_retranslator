# client

import sys
import socket
import argparse
from random import randint
from utils import get_message, send_message

test_data = '74000000333533393736303133343435343835004B0BFB70000000030BBB000000270102706F73696E666F00A027AFDF5D9848403AC7253383DD4B400000000000805A40003601460B0BBB0000001200047077725F657874002B8716D9CE973B400BBB00000011010361766C5F696E707574730000000001'


def create_msg(test_data):
    message_output = {
        'test_data': test_data,
        'device_id': randint(2000, 3000),
    }
    return message_output


def client_main():
    for_parse = argparse.ArgumentParser()
    for_parse.add_argument('port', nargs='?', type=int, default='7777')
    for_parse.add_argument('address', nargs='?', type=str, default='127.0.0.1')

    args_parse = for_parse.parse_args()

    try:
        server_port = args_parse.port
        server_address = args_parse.address
        if not (1024 < server_port < 65535):
            raise ValueError
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    trans_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trans_port.connect((server_address, server_port))
    message_to_server = create_msg(test_data)
    send_message(trans_port, message_to_server)


if __name__ == '__main__':
    client_main()
