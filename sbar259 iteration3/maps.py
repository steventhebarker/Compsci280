class Map(object):
    """ Stores details on a map. """

    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath


class MapStore(object):
    """ MapStore stores all the maps for DALSys. """

    def __init__(self, conn=None):
        self._maps = {}
        self._conn = conn

    def add(self, map):
        """ Adds a new map to the store. """
        if map.name in self._maps:
            raise Exception('Map already exists in store')
        self._maps[map.name] = map

    def remove(self, map):
        """ Removes a map from the store. """
        if map.name not in self._maps:
            raise Exception('map does not exist in store')
        del self._maps[map.name]

    def get(self, name):
        """ Retrieves a map from the store by its name. """
        if name not in self._maps:
            raise Exception('Map is not in the store')
        
        return self._maps[name]

    def list_all(self):
        """ Lists all the maps in the store. """
        for name in self._maps:
            yield name

    def save(self):
        """ Saves the store to the database. """
        pass    # TODO: we don't have a database yet
