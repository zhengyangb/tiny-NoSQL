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

    @app.route('/<string:collection>/<uuid:doc_id>', methods=['GET'])
    def collection_find_by_id(collection, doc_id):
        """
        Return the document specified by collection name and document id.
        """

        try:
            table = database.get_collection(collection)
        except KeyError:
            return '''
            Not found.
            The collection \"{}\" is not found. Please check again the name of the collection. 
            You can use /show_collections to find all collections in the database.
            '''.format(collection), 404

        rtn = table.find({'_id': str(doc_id)})
        if rtn['successful']:
            if rtn['results']['doc']:
                return jsonify(rtn['results']['doc'][0])
            else:
                return 'Document not found', 404
        else:
            return rtn['message'], 406



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
            if not query:
                return "Find query can't be empty. Please use _all to query all data.", 400
            rtn = table.find(query)
            if rtn['successful']:
                return jsonify(rtn['results'])
            else:
                return rtn['message'], 406
        # Query string version
        else:
            query = dict(request.args)
            if not query:
                return "Find query can't be empty. Please use _all to query all data.", 400
            for k in query:
                if isinstance(query[k], str) and query[k].isnumeric():
                    query[k] = eval(query[k])
            rtn = table.find(query)
            if rtn['successful']:
                return jsonify(rtn['results'])
            else:
                return rtn['message'], 406

    @app.route('/<string:collection>/_update', methods=['PUT', 'POST'])
    def collection_update(collection):
        """
        Update the documents matching query criterion with set, unset, increment, or append
        """

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
            if not query:
                return "Find query can't be empty. Please use _all to query all data.", 400
            if 'criteria' not in query or 'operation' not in query:
                return "An update request needs to have \"criteria\" and \"operation\" specified", 400
            rtn = table.update(query['criteria'], query['operation'])
            if rtn['successful']:
                return jsonify(rtn['doc_id'])
            else:
                return 'Updated {} documents, {} fail.'.format(rtn['successful_cnt'], rtn['unsuccessful_cnt']), 406
        # Query string version
        else:
            query = dict(request.args)
            if not query:
                return "Find query can't be empty. Please use _all to query all data.", 400
            for k in query:
                if isinstance(query[k], str) and query[k].isnumeric():
                    query[k] = eval(query[k])
            rtn = table.update(query['criteria'], query['operation'])
            if rtn['successful']:
                return jsonify(rtn['doc_id'])
            else:
                return 'Updated {} documents, {} fail.'.format(rtn['successful_cnt'], rtn['unsuccessful_cnt']), 406

    @app.route('/<string:collection>/_insert', methods=['POST'])
    def collection_insert(collection):
        """
        Insert one or a list of documents to the collection.
        """

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
            doc = request.json
        # Query string version
        else:
            doc = dict(request.args)
            if isinstance(doc, dict):
                for k in doc:
                    if isinstance(doc[k], str) and doc[k].isnumeric():
                        doc[k] = eval(doc[k])
        if not isinstance(doc, (dict, list)):
            return "Please either insert a document or an array of document", 400
        if isinstance(doc, dict):
            rtn = table.insert(doc)
        elif isinstance(doc, list):
            rtn = table.insert_many(doc)
        if rtn['successful']:
            return jsonify(rtn['doc_id'])
        else:
            return rtn['message'], 406

    @app.route('/<string:collection>/_remove', methods=['DELETE'])
    def collection_remove(collection):
        """
        Remove all documents meeting the criterion
        """

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
            if not query:
                return "Find query can't be empty. Please use _all to query all data.", 400
        # Query string version
        else:
            query = dict(request.args)
            if not query:
                return "Find query can't be empty. Please use _all to query all data.", 400
            for k in query:
                if isinstance(query[k], str) and query[k].isnumeric():
                    query[k] = eval(query[k])
        rtn = table.remove(query)
        if rtn['successful']:
            return jsonify(rtn['doc_id'])
        else:
            return rtn['message'], 406


    return app
