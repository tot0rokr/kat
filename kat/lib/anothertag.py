class Tag:
    """
    Instance Field:

    name: name of tag
    loc:  defined location
        path: in path of file
        adderss: line number or regular expression in other to find tag on file of path
    contents: contents
    stype: type of tag (like datatype, function, macro, etc..)
    """

    def __init__(self, name, loc, cont, stype):
        self.__data = {}
        if name is not None:
            self.__data['name'] = name
        else:
            self.__data['name'] = ""

        if loc is not None:
            self.__data['loc'] = loc
            if 'path' not in loc:
                self.__data['loc']['path'] = None
            if 'address' not in loc:
                self.__data['loc']['address'] = None
        else:
            self.__data['loc'] = {'path': None, 'address': None}

        if cont is not None:
            self.__data['contents'] = cont
        else:
            self.__data['contents'] = None

        if stype is not None:
            self.__data['stype'] = stype
        else:
            self.__data['stype'] = ""

    def update(self, name, loc, cont, stype):
        if name is not None:
            self.__data['name'] = name

        if defloc is not None:
            self.__data['loc'] = loc

        if cont is not None:
            self.__data['contents'] = cont

        if stype is not None:
            self.__data['stype'] = stype

    #  def get(self):
        #  return self.__data

    def show(self):
        print(self.__data['name'], end=' ')
        print(self.__data['stype'], end=' ')
        print(self.__data['loc']['path'], end=' ')
        print(self.__data['loc']['address'])
        print(self.__data['contents'], end=' ')

