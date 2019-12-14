import uuid
from query import Query
from operation import DocOperation


def check_value_valid(value):
    # Array
    if isinstance(value, list):
        return all((check_value_valid(v) for v in value))
    # Dict
    if isinstance(value, dict):
        return check_document_valid(value)
    # Primitives
    return value is None or isinstance(value, (str, float, int, bool))


def check_document_valid(doc):
    if not isinstance(doc, dict):
        return False
    for k, v in doc.items():
        if '/' in k or '.' in k or k[0] == '_':
            return False
        if not check_value_valid(v):
            return False
    return True


# We only have implemented per-field query. Combination of multiple fields is yet to be implemented
def check_and_preprocess_query(query):
    if not isinstance(query, dict):
        return False, None
    processed_query = Query(query)
    return True, processed_query


def check_and_preprocess_command(command):
    allowed_command = ['_set', '_unset', '_append', '_increment']
    if  not isinstance(command, dict):
        return False, None
    if any(k not in allowed_command for k in command.keys()):
        return False, None
    processed_command = DocOperation(command)
    return True, processed_command



# TODO Query and Projection Operators to implement:
# Comparison eq, gt, gte, lt, lte, ne, in, nin
# Logical or, and ...



def generate_doc_id(table):
    while True:
        doc_id = str(uuid.uuid4())
        if doc_id not in table:
            return doc_id
    return doc_id


def insert(table, doc):
    if not check_document_valid(doc):
        return False, 'document invalid'
    doc_id = generate_doc_id(table)
    table[doc_id] = doc
    return True, doc_id


def insert_many(table, docs):
    if not all([check_document_valid(doc) for doc in docs]):
        return False, 'some or all document invalid'
    doc_ids = []
    for doc in docs:
        doc_id = generate_doc_id(table)
        table[doc_id] = doc
        doc_ids.append(doc_id)
    return True, doc_ids


def find(table, query):
    success, query = check_and_preprocess_query(query)
    if not success:
        return False, 'your query has wrong syntax'

    res_id = []
    res = []

    for doc_id, doc in table.items():
        if query(doc_id, doc):
            res_id.append(doc_id)
            res.append(doc)
    return True, (res, res_id)


def update(table, query, command):
    """
    :param table: The collection dictionary
    :param query: the documents to be updated
    :param command: update content
    :return: successful, message/updated documents
    """
    success, query = check_and_preprocess_query(query)
    if not success:
        return False, 'your query has wrong syntax'

    success, command = check_and_preprocess_command(command)
    if not success:
        return False, 'your update command has wrong syntax'

    successful_doc_id = []
    unsuccessful_doc_id = []

    for doc_id, doc in table.items():
        if query(doc_id, doc):
            if command(doc):
                successful_doc_id.append(doc_id)
            else:
                unsuccessful_doc_id.append(doc_id)

    if not unsuccessful_doc_id:
        return True, successful_doc_id
    else:
        return False, (successful_doc_id, unsuccessful_doc_id)


def remove(table, query):
    """
    Remove documents selected by query from table
    :param table: dictionary
    :param query: dictionary
    :return:
    """
    success, query = check_and_preprocess_query(query)
    if not success:
        return False, 'your query has wrong syntax'

    res_id = []

    for doc_id, doc in table.items():
        if query(doc_id, doc):
            del table[doc_id]
    return True, res_id

