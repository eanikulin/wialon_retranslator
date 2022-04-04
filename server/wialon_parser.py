import binascii
import struct


def parse(fmt, binary, offset=0):
    parsed = struct.unpack_from(fmt, binary, offset)
    return parsed[0] if len(parsed) == 1 else parsed


def parsePacket(packet):
    msg = {
        'id': 0,
        'time': 0,
        'flags': 0,
        'params': {},
        'blocks': []
    }

    controller_id_size = packet.find(b'\x00', 8)
    (msg['id'], msg['time'], msg['flags']) = parse('> %ds x i i' % (controller_id_size), packet)

    data_blocks = packet[controller_id_size + 1 + 4 + 4:]

    while len(data_blocks):
        offset = 2 + 4 + 1 + 1
        name_size = data_blocks.find(b'\x00', offset) - offset
        (block_type, block_length, visible, data_type, name) = parse('> h i b b %ds' % (name_size), data_blocks)

        block = {
            'type': block_type,
            'length': block_length,
            'visibility': visible,
            'data_type': data_type,
            'name': name
        }

        block['data_block'] = data_blocks[offset + name_size + 1:block_length * 1 + 6]

        v = ''
        if data_type:
            if name == b'posinfo':
                v = {'lat': 0, 'lon': 0, 'a': 0, 's': 0, 'c': 0, 'sc': 0}
                (v['lon'], v['lat'], v['a']) = parse('d d d', block['data_block'])
                (v['s'], v['c'], v['sc']) = parse('> h h b', block['data_block'], 24)

        msg['params'][name] = v
        data_blocks = data_blocks[block_length + 6:]

    return msg


def parse_message(message):
    return parsePacket(binascii.unhexlify(message))
