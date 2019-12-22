import sys
from database import Database
from router import make_app


def main(argv):
    assert argv[0], 'Please specify the directory of the database'
    db = Database(argv[0])
    app = make_app(db)
    # db.create_collection('fruits', overwrite=True)
    # table = db.get_collection('fruits')
    # table.insert_many([{'type': 'apple', 'price': [100, 11, 12]},
    #                          {'type': 'banana', 'price': 100, 'nutrition': {'Vitamin_C': 100, 'Cal': 10}}])
    app.run(debug=True, port=9020)
    while True:
        try:
            print('Press Ctrl+C to exit and save.')
            input()
        except (EOFError,KeyboardInterrupt):
            db.close()
            print('Database saved.')
            exit()


if __name__ == '__main__':
    main(sys.argv[1:])
