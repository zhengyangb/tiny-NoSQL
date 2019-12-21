import sys, os
from database import Database
from router import make_app


def main(argv):
    assert argv[0], 'Please specify the directory of the database'
    global db
    db = Database(argv[0])
    app = make_app(db)

    # global data
    # if os.path.isfile(argv[0]):
    #     data = pickle.load(open(argv[0], 'rb'))
    #     assert type(data) is dict, 'The data file needs to be implemented with dict'
    # else:
    #     data = dict()

    # app.run(debug=True, port=9020)

    # while True:
    #     conn, addr = s.accept()
    #     try:
    #         cmd, key, value = parse_raw_command(conn.recv(1024).decode())
    #         # print(cmd, key, value)
    #     except (AssertionError, ValueError):
    #         print('Your command has wrong syntax. Please check and input again. ')
    #         continue
    #     if cmd in ('STOP', 'EXIT'):
    #         break
    #     success, rtn = db_operation[cmd](key, value)
    #     if success:
    #         conn.sendall(rtn)
    #     conn.close()

    # pickle.dump(data, open(argv[0], 'wb'))
    # print('Data written to {}'.format(argv[0]))

    db.create_collection('fruits', overwrite=True)
    table = db.get_collection('fruits')

    # print(table.all())
    # print(table.insert_many([{'type': 'apple', 'price': [100, 11, 12]},
    #                          {'type': 'banana', 'price': 100, 'nutrition': {'Vitamin_C': 100, 'Cal': 10}}]))
    # print(table.insert({'type': {'_lt':1}}))
    # print(table.all())
    # print()
    # print(table.find({'price': 12}))
    # print(table.update({'price': 12}, {'_set': {'nutrition': {'Vitamin_C': 15}},
    #                                    '_append': {'price': 15}}))
    #
    # print(table.remove({'nutrition.Vitamin_C': {'_gt': 20}}))
    #
    # print(len(table))
    # print(len(db.fruits))
    # db.close()
    table.insert_many([{'type': 'apple', 'price': [100, 11, 12]},
                             {'type': 'banana', 'price': 100, 'nutrition': {'Vitamin_C': 100, 'Cal': 10}}])
    print(table.all(show_doc_id=True))
    app.run(debug=True, port=9020)


if __name__ == '__main__':
    main(sys.argv[1:])
