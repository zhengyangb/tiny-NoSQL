from functools import partial, reduce
import operator


def nested_dict_check(dictionary, keys):
    """
    Check if a list of keys exists in the nested dictionary
    :param dictionary:
    :param keys: A list of keys
    :return: True the key exists in dictionary
    """
    if not isinstance(dictionary, dict):
        return False
    try:
        reduce(operator.getitem, keys, dictionary)
        return True
    except (KeyError, IndexError):
        return False


def nested_dict_get(dictionary, keys):
    """
    If the key does not exist, it will throw an error.
    :param dictionary:
    :param keys: A list of keys
    :return: The value of keys specified
    """
    return reduce(operator.getitem, keys, dictionary)


def nested_dict_write(dictionary, keys, value, create_if_not_exist=True):
    # To be implemented
    pass


class Query:
    comparison_operations = ['_eq', '_gt', '_ge', '_lt', '_le', '_ne', '_in', '_nin']

    # TODO Check type before doing operation or catch TypeError exception


    oper2func = dict()
    oper2func['_eq'] = lambda b: lambda x: operator.eq(x, b)
    oper2func['_lt'] = lambda b: lambda x: isinstance(x, (int, float)) and isinstance(b, (int, float)) and operator.lt(x, b)
    oper2func['_le'] = lambda b: lambda x: isinstance(x, (int, float)) and isinstance(b, (int, float)) and operator.le(x, b)
    oper2func['_ne'] = lambda b: lambda x: operator.ne(x, b)
    oper2func['_ge'] = lambda b: lambda x: isinstance(x, (int, float)) and isinstance(b, (int, float)) and operator.ge(x, b)
    oper2func['_gt'] = lambda b: lambda x: isinstance(x, (int, float)) and isinstance(b, (int, float)) and operator.gt(x, b)
    oper2func['_in'] = lambda b: lambda x: (isinstance(b, list) or (isinstance(b, str) and isinstance(x, str))) and operator.contains(b, x)
    oper2func['_nin'] = lambda b: lambda x: (isinstance(b, list) or (isinstance(b, str) and isinstance(x, str))) and not operator.contains(b, x)

    def __init__(self, query):
        # Check query format

        # Parse each query condition
        self.cond = []
        for k, v in query.items():
            if k == '_id':
                # partial will store the parameter, instead of closure
                self.cond.append(partial(Query.condition_doc_id_is, truth=v))
            else:
                k = k.split('.')
                if Query.is_value_valid_comparison_condition(v):
                    self.cond.append(partial(Query.condition_value_satisfy, k=k, v=Query.comparison2func(v)))
                else:
                    self.cond.append(partial(Query.condition_value_is_or_in, k=k, v=v))
        # For comparison condition

        return

    def __call__(self, doc_id, doc):
        return all(cond(doc_id, doc) for cond in self.cond)


    @staticmethod
    def condition_doc_id_is(doc_id, doc, truth=None):
        return doc_id == truth

    @staticmethod
    def condition_value_is_or_in(doc_id, doc, k=None, v=None):
        """
        Check if doc[k] == v or v is in doc[k].
        :param doc_id: will not be used
        :param doc: document to check
        :param k: list of keys.
        :param v: The correct answer
        :return:
        """
        if k is None:
            raise RuntimeError('must bind before calling')
        if not nested_dict_check(doc, k):
            return False
        doc_value = nested_dict_get(doc, k)
        if doc_value == v:
            return True
        if isinstance(doc_value, list) and v in doc_value:
            return True

    @staticmethod
    def condition_value_satisfy(doc_id, doc, k=None, v=None):
        """
        Check if doc[k] satisfy the requirements in v.
        :param doc_id: will not be used
        :param doc: document to check
        :param k: list of keys.
        :param v: function
        :return:
        """
        if k is None:
            raise RuntimeError('must bind before calling')
        if not nested_dict_check(doc, k):
            return False
        doc_value = nested_dict_get(doc, k)
        return v(doc_value)


    @staticmethod
    def is_value_valid_comparison_condition(value):
        return isinstance(value, dict) and all((k in Query.comparison_operations for k in value.keys()))

    @staticmethod
    def comparison2func(comp_cond):
        """
        Input a dict of comparison conditions, output a function(v) stating whether v satisfies comp_cond
        :param comp_cond: This must satisfy Query.is_value_valid_comparison_condition
        :return: A function
        """
        cond = [Query.oper2func[k](v) for k, v in comp_cond.items()]
        # TODO Support logic and nested conditions

        def check_comparison_condition(value):
            return all((c(value) for c in cond))

        return check_comparison_condition



