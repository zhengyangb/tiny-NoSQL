import controller
import warnings

# TODO this is an user-facing module, but will also be used in REST api.


class Collection:

    def __init__(self, table):
        self.__table = table  # Reference of original database
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

    def find(self, query):
        success, rtn = controller.find(self.__table, query)
        if success:
            return rtn[0]
        else:
            return {'successful': False, 'message': rtn}

    def update(self, query, command):
        success, rtn = controller.update(self.__table, query, command)
        if success:
            return {'successful': True, 'doc_id': rtn}
        else:
            return {'successful': False,
                    'successful_cnt': len(rtn[0]),
                    'unsuccessful_cnt': len(rtn[1])}

    def remove(self, query):
        success, rtn = controller.remove(self.__table, query)
        if success:
            return {'successful': True, 'doc_id': rtn}
        else:
            return {'successful': False, 'message': rtn}
