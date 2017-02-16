from collections import namedtuple


class User(namedtuple('User', ['id', 'first_name', 'last_name',
                                'username', 'email', 'password', 'password_salt'])):

    def __init__(self):
        self.data = None
        self.return_user = None

    def map_to_data(self, row):
        self.data._make(row)
        return self.data

    '''__slots = ()

    _fields = ('id', 'first_name', 'last_name',
               'username', 'email', 'password', 'password')

    def __new__(_cls, id, first_name, last_name, username, email, password, password_salt):
        return _tuple.__new__(_cls, (id, first_name, last_name, username, email, password, password_salt))

    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        'Make a new Point object from a sequence or iterable'
        result = new(cls, iterable)
        print result
        if len(result) != 7:
            raise TypeError('Expected 2 arguments, got %d' % len(result))
        return result

    def __repr__(self):
        return 'User(id=%r, first_name=%r, last_name=%r, username=%r, email=%r, password=%r, password_salt=%r)'

    def _asdict(self):
        return OrderedDict(zip(self._fields, self))

    def _replace(_self, **kwds):
        'Return a new Point object replacing specified fields with new values'
        result = _self._make(map(kwds.pop, ('id', 'first_name', 'last_name',
                   'username', 'email', 'password', 'password'), _self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % kwds.keys())
        return result

    def __getnewargs__(self):
        return tuple(self)

    def __getstate__(self):
        pass'''

    # def __init__(self, id, first_name, last_name, username, email, password, password_salt):
    #    self.id = id
    #    self.first_name = first_name
    #    self.last_name = last_name
    #    self.username = username
    #    self.email = email
    #    self.password = password
    #    self.password_salt = password_salt
