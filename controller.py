import uuid


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

def check_and_preprocess_query(query):
    if not isinstance(query, dict):
        return False, None
    processed_query = {}
    for k, v in query.items():
        k = k.split('.')
        if


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
