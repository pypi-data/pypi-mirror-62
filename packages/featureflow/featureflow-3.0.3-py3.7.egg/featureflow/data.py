from io import StringIO, BytesIO
from uuid import uuid4
import os


class IdProvider(object):
    """
    Marker class for object that returns new ids
    """

    def new_id(self):
        raise NotImplemented()


class UuidProvider(IdProvider):
    def __init__(self):
        super(UuidProvider, self).__init__()

    def new_id(self, **kwargs):
        return uuid4().hex


class IntegerIdProvider(IdProvider):
    def __init__(self):
        super(IntegerIdProvider, self).__init__()
        self._id = 1

    def new_id(self, **kwargs):
        self._id += 1
        return self._id - 1


class UserSpecifiedIdProvider(IdProvider):
    def __init__(self, key=None):
        super(UserSpecifiedIdProvider, self).__init__()
        if not key:
            raise ValueError('key must be provided')
        self._key = key

    def new_id(self, **kwargs):
        return kwargs[self._key]


class StaticIdProvider(IdProvider):
    def __init__(self, key):
        self.key = key

    def new_id(self, **kwargs):
        return self.key


class KeyBuilder(object):
    """
    Marker class for an algorithm to build keys
    from "document" id and feature name
    """

    def build(self, *args):
        raise NotImplemented()

    def decompose(self, composed):
        raise NotImplemented()


class StringDelimitedKeyBuilder(KeyBuilder):
    def __init__(self, seperator=':'):
        super(StringDelimitedKeyBuilder, self).__init__()
        self._seperator = seperator

    def build(self, *args):
        return self._seperator.join(str(x) for x in args)

    def decompose(self, composed):
        return composed.split(self._seperator)


class Database(object):
    """
    Marker class for a datastore
    """

    def __init__(self, key_builder=None):
        super(Database, self).__init__()
        self.key_builder = key_builder

    # TODO: Maybe this should just be open(), since it returns a file-like 
    # object
    def write_stream(self, key, content_type):
        raise NotImplemented()

    # TODO: Maybe this should just be open(), since it returns a file-like
    # object
    def read_stream(self, key):
        raise NotImplementedError()

    def random(self):
        """
        Return the read stream of a random key
        """
        raise NotImplementedError()

    def size(self, key):
        raise NotImplementedError()

    def iter_ids(self):
        raise NotImplementedError()

    def __iter__(self):
        return self.iter_ids()

    def __contains__(self, key):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()


class IOWithLength(BytesIO):
    def __init__(self, content):
        super().__init__(content)
        self._length = len(content)

    def __len__(self):
        return self._length


class InMemoryDatabase(Database):
    def __init__(self, key_builder=None):
        super(InMemoryDatabase, self).__init__(key_builder=key_builder)
        self._dict = dict()

    def write_stream(self, key, content_type):
        bio = BytesIO()
        self._dict[key] = bio

        def hijacked_close():
            bio.seek(0)
            self._dict[key] = bio.read()
            bio._old_close()

        bio._old_close = bio.close
        bio.close = hijacked_close
        return bio

    def read_stream(self, key):
        return IOWithLength(self._dict[key])

    def size(self, key):
        return len(self._dict[key])

    def iter_ids(self):
        seen = set()
        for key in list(self._dict.keys()):
            _id, _, _ = self.key_builder.decompose(key)
            if _id in seen:
                continue
            yield _id
            seen.add(_id)

    def __contains__(self, key):
        return key in self._dict

    def __delitem__(self, key):
        del self._dict[key]


class LazyFile(object):
    """
    A file wrapper that won't create a file until some bytes have been written
    """

    def __init__(self, path):
        super(LazyFile, self).__init__()
        self.path = path
        self._file = None

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        if self._file is None:
            return
        self._file.close()

    def close(self):
        if self._file is None:
            return
        return self._file.close()

    def write(self, data):
        if not data:
            return

        if self._file is None:
            self._file = open(self.path, 'wb')
        try:
            self._file.write(data.encode())
        except AttributeError:
            self._file.write(data)


class FileSystemDatabase(Database):
    def __init__(self, path=None, key_builder=None, createdirs=False):
        super(FileSystemDatabase, self).__init__(key_builder=key_builder)
        self._path = path
        if createdirs and not os.path.exists(self._path):
            os.makedirs(self._path)

    def write_stream(self, key, content_type):
        return LazyFile(os.path.join(self._path, key))

    def read_stream(self, key):
        try:
            return open(os.path.join(self._path, key), 'rb')
        except IOError:
            raise KeyError(key)

    def size(self, key):
        path = os.path.join(self._path, key)
        try:
            return os.stat(path).st_size
        except OSError:
            raise KeyError(key)

    def iter_ids(self):
        seen = set()
        for fn in os.listdir(self._path):
            _id, _, _ = self.key_builder.decompose(fn)
            if _id in seen:
                continue
            yield _id
            seen.add(_id)

    def __contains__(self, key):
        path = os.path.join(self._path, key)
        return os.path.exists(path)

    def __delitem__(self, key):
        path = os.path.join(self._path, key)
        os.remove(path)
