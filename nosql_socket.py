import sys, os, pickle
import socket


def parse_raw_command(raw_command):
    commands = []
    start = 0
    for i, c in enumerate(raw_command):
        if c == ' ':
            if i > start:
                commands.append(raw_command[start:i])
            start = i+1
    if start != len(raw_command):
        commands.append(raw_command[start:len(raw_command)])

    cmd, key, value, type = commands + [None] * (4 - len(commands))
    cmd = cmd.upper()


    if cmd.upper() in ('GET', 'INCREMENT', 'DELETE'):
        assert key is not None
    elif cmd.upper() in ('PUT', 'APPEND'):
        assert key is not None and value is not None and type is not None and type.lower() in ('int', 'array', 'str')
        type = type.lower()
        if type in ('int', 'str'):
            value = eval(type)(value)
        elif type == 'array':
            # TODO Support for specifying type in array
            value = [word.strip() for word in value.split(',')]

    return cmd, key, value


def db_operation_get(key, *args):
    if key in data:
        return (True, data[key])
    else:
        print('[Error] Key {} not found, please check the key name.'.format(key))
        return (False, None)

def db_operation_put(key, value):
    if key in data:
        print('[Warining] Key {} exists. Overwriting current data.')
    data[key] = value
    return (True, '{key}: {value}'.format(key=key, value=value))

def db_operation_delete(key, *args):
    if key not in data:
        print('[Error] Key {} not found, please check the key name.'.format(key))
        return (False, None)
    else:
        del data[key]
        return (True, '{} is deleted'.format(key))

def db_operation_append(key, value):
    success, pointer = db_operation_get(key)
    if not success:
        return False, None
    if type(pointer) is not list:
        print('[Error] value of {} is not an array.'.format(key))
        return False, None
    pointer.append(value)
    return True, pointer


def db_operation_increment(key):
    success, pointer = db_operation_get(key)
    if not success:
        return False, None
    if type(pointer) is not int:
        print('[Error] value of {} is not an integer.'.format(key))
        return False, None
    data[key] += 1
    return True, '{key}: {value}'.format(key=key, value=data[key])

db_operation = {
    'GET': db_operation_get,
    'PUT': db_operation_put,
    'DELETE': db_operation_delete,
    'APPEND': db_operation_append,
    'INCREMENT': db_operation_increment,
}



def main(argv):
    assert argv[0], 'Please specify the directory of the database'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 9010))
    s.listen()

    global data
    if os.path.isfile(argv[0]):
        data = pickle.load(open(argv[0], 'rb'))
        assert type(data) is dict, 'The data file needs to be implemented with dict'
    else:
        data = dict()

    while True:
        conn, addr = s.accept()
        try:
            cmd, key, value = parse_raw_command(conn.recv(1024).decode())
            # print(cmd, key, value)
        except (AssertionError, ValueError):
            print('Your command has wrong syntax. Please check and input again. ')
            continue
        if cmd in ('STOP', 'EXIT'):
            break
        success, rtn = db_operation[cmd](key, value)
        if success:
            conn.sendall(rtn)
        conn.close()

    s.close()
    pickle.dump(data, open(argv[0], 'wb'))
    print('Data written to {}'.format(argv[0]))






if __name__ == '__main__':
    main(sys.argv[1:])