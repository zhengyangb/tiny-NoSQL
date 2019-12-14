import os
import json
from collection import Collection


class Database:
    def __init__(self, location):
        self.__active = True
        self.__db = None
        self.__location = location

        if os.path.isfile(self.__location):
            self.__db = json.load(open(self.__location))
        else:
            print('File does not exist. Will create and save to the location specified.')
            self.__db = {'main': {}}

    def create_collection(self, table_name, overwrite=False):
        if table_name in self.__db and not overwrite:
            raise KeyError('Collection already exists')
        if table_name in dir(self):
            raise KeyError('Collection name invalid')
        self.__db[table_name] = {}
        return Collection(self.__db[table_name])

    def get_collection(self, table_name):
        if table_name in self.__db:
            return Collection(self.__db[table_name])
        else:
            raise KeyError('Collection name not found')

    def show_collections(self):
        return list(self.__db.keys())

    def close(self):
        json.dump(self.__db, open(self.__location, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        self.__db = None
        self.__active = False
        return

    def __getattr__(self, item):
        """
        Only called if attribute not found.
        Used for shortcut of creating a Collection object of the collection
        :param item: collection name
        :return:
        """
        if item in self.__db.keys():
            return Collection(self.__db[item])
        else:
            raise AttributeError()