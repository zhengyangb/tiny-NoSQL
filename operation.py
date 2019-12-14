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


class DocOperation:
    def __init__(self, command):
        self.__oper_set = None
        self.__oper_unset = None
        self.__oper_increment = None
        self.__oper_append = None

        if '_set' in command and check_document_valid(command['_set']):
            self.__oper_set = command['_set']
        if '_unset' in command and isinstance(command['_unset'], list):
            self.__oper_unset = command['_unset']
        if '_increment' in command and isinstance(command['_increment'], list):
            self.__oper_increment = command['_increment']
        if '_append' in command and isinstance(command['_append'], dict):
            self.__oper_append = command['_append']
        return

    def __call__(self, doc):
        """
        Apply predetermined operations on doc
        :param doc:
        :return:
        """
        try:
            if self.__oper_set:
                self.apply_set(doc)
            if self.__oper_unset:
                self.apply_unset(doc)
            if self.__oper_increment:
                self.apply_increment(doc)
            if self.__oper_append:
                self.apply_append(doc)
            return True
        except (KeyError, ValueError):
            return False

    def apply_set(self, doc):
        for k, v in self.__oper_set.items():
            doc[k] = v
        return

    def apply_unset(self, doc):
        for k in self.__oper_unset:
            del doc[k]
        return

    def apply_increment(self, doc):
        for k in self.__oper_increment:
            if not isinstance(doc[k], (float, int)):
                raise ValueError
            doc[k] += 1
        return

    def apply_append(self, doc):
        for k, v in self.__oper_append.items():
            if not isinstance(doc[k], list):
                raise ValueError
            doc[k].append(v)
        return
