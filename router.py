from flask import Flask, jsonify, abort, request

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def make_app(database):
    app = Flask(__name__)


    @app.route('/')
    def index():
        return "Hello, World!"

    @app.route('/hello')
    def hello():
        return jsonify({
            'greetings': 'Hi! This is TinyNoSQL',
            'database_ready': bool(database),
        })

    @app.route('/show_collections', methods=['GET'])
    def show_collections():
        return jsonify(database.show_collections())

    @app.route('/<string:collection>/_all', methods=['GET'])
    def collection_all(collection):
        """
        Return all documents in the given collection.
        """
        try:
            table = database.get_collection(collection)
        except KeyError:
            return '''
            Not found.
            The collection \"{}\" is not found. Please check again the name of the collection. 
            You can use /show_collections to find all collections in the database.
            '''.format(collection), 404
        return jsonify(table.all())

    @app.route('/<string:collection>/_find', methods=['GET', 'POST'])
    def collection_find(collection):
        """
        Find all documents in the given collection matching the given criterion
        """
        # Like elasticsearch's API, we try to implement a lite api using query-string (URL parameters) and a full
        # function request body using JSON

        try:
            table = database.get_collection(collection)
        except KeyError:
            return '''
            Not found.
            The collection \"{}\" is not found. Please check again the name of the collection. 
            You can use /show_collections to find all collections in the database.
            '''.format(collection), 404

        # Full request body version
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            query = request.json
            rtn = table.find(query)
            if rtn['successful']:
                return jsonify(rtn['results'])
            else:
                return rtn['message'], 406
        else:
            query = dict(request.args)
            rtn = table.find(query)
            if rtn['successful']:
                return jsonify(rtn['results'])
            else:
                return rtn['message'], 406



    return app
