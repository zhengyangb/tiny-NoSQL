import controller
import warnings

# TODO this is an user-facing module, but will also be used in REST api.


class Collection:

    def __init__(self, table):
        self.__table = table
        return

    def __len__(self):
        return len(self.__table)

    def all(self):
        return list(self.__table.values())

    def insert(self, doc):
        success, rtn = controller.insert(self.__table, doc)
        if success:
            return {'successful': True, 'doc_id': rtn}
        else:
            return {'successful': False, 'message': rtn}

    def insert_many(self, docs):
        success, rtn = controller.insert_many(self.__table, docs)
        if success:
            return {'successful': True, 'doc_id': rtn}
        else:
            return {'successful': False, 'message': rtn}
